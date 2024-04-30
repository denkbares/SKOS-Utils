import os
import uuid
from datetime import datetime

from rdflib import URIRef, RDF, Literal, Graph, RDFS, PROV, XSD, BNode
from rdflib.namespace import SKOS, Namespace
from rdflib import namespace

from SKOSUtils.Converter.ProcessUtils import ProcessUtils


class Generic2SKOS:
    def __init__(self, local_namespace, scheme_name, bindings={}, default_language='de'):
        self.default_language = default_language
        self.scheme_name = scheme_name
        self.namespace = local_namespace
        self.scheme = None
        self.created_concepts = {}
        self.bindings = bindings
        self.order_prop = namespace.SH.order
        self.source_filename = 'Source filename undefined'
        self.source_filename_changed = None

    def create_scheme_uri(self, graph):
        schemename = self.scheme_name
        su = URIRef(self.namespace + schemename)
        graph.add((su, RDF.type, SKOS.ConceptScheme))
        graph.add((su, SKOS.prefLabel, Literal(schemename, self.default_language)))
        graph.add((su, SKOS.prefLabel, Literal(schemename)))
        return su

    def add_binding(self, abbr, uri):
        self.bindings[uri] = abbr

    def to_rdf(self, scheme, out_filename, serialize_format='turtle'):
        self.created_concepts = {}
        graph = Graph()
        skos_ns = Namespace(SKOS)
        graph.bind("skos", skos_ns)
        graph.bind("sh", namespace.SH)
        scheme.scheme_uri = self.create_scheme_uri(graph, scheme)
        for babbr, buri in self.bindings.items():
            graph.bind(buri, babbr)
        for tc in scheme.top_concepts:
            self.instantiate_rec(tc, graph)
        graph.serialize(format=serialize_format, destination=out_filename)

    def create_scheme_uri(self, graph, scheme):
        schemename = scheme.name
        su = URIRef(self.namespace + schemename)
        graph.add((su, RDF.type, SKOS.ConceptScheme))
        graph.add((su, SKOS.prefLabel, Literal(schemename, self.default_language)))
        graph.add((su, SKOS.prefLabel, Literal(schemename)))
        # Also add some PROV information
        graph.add((su, RDF.type, PROV.entity))
        graph.add((su, PROV.generatedAtTime, Literal(scheme.generation_time, datatype=XSD.dateTime)))
        run_activity = URIRef(self.namespace + 'SKOS-Utils-Run')
        graph.add((su, PROV.wasGeneratedBy, run_activity))
        graph.add((run_activity, RDF.type, PROV.activity))
        graph.add((run_activity, SKOS.prefLabel, Literal('SKOS-Utils Run')))

        source_entity = BNode()
        graph.add((run_activity, PROV.used, source_entity))
        graph.add((source_entity, RDF.type, PROV.entity))
        graph.add((source_entity, PROV.value, Literal(self.source_filename)))
        if self.source_filename_changed:
            graph.add((source_entity, PROV.generatedAtTime, Literal(self.source_filename_changed, datatype=XSD.dateTime)))

        return su

    def set_source_filename(self, filename):
        """
        Get the modified date of the specified filename
        """
        self.source_filename = filename
        stats = os.stat(filename)
        self.source_filename_changed = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%dT%H:%M:%S")

    def instantiate_notes(self, graph, uri, concept):
        for note in concept.notes:
            graph.add((uri, SKOS.note, Literal(note)))

    def instantiate_external_properties(self, graph, uri, concept):
        """Template method for overwriting classes, that can export additional properties for this URI"""
        pass

    def instantiate_rec(self, concept, graph):
        if concept.uri:
            uri = concept.uri
        else:
            uri = URIRef(uuid.uuid4())
        self.created_concepts[uri] = uri
        graph.add((uri, RDF.type, SKOS.Concept))

        self.add_properties(graph, concept, uri)

        if (uri, SKOS.prefLabel, None) not in graph:
            graph.add((uri, SKOS.prefLabel, Literal(concept.name, lang=self.default_language)))
            graph.add((uri, SKOS.prefLabel, Literal(concept.name)))

        if concept.notes:
            self.instantiate_notes(graph, uri, concept)
        self.instantiate_external_properties(graph, uri, concept)

        graph.add((uri, SKOS.inScheme, self.scheme.scheme_uri))

        if concept.hiddenLabel:
            graph.add((uri, SKOS.hiddenLabel, Literal(concept.hiddenLabel)))
        if concept.order:
            graph.add((uri, self.order_prop, Literal(concept.order)))

        # add exact matches
        for em in concept.exact_matches:
            if isinstance(em, URIRef):
                em_uri = em
            else:
                em_uri = URIRef(str(em))
            graph.add((uri, SKOS.exactMatch, em_uri))

        for b in concept.broader:
            graph.add((uri, SKOS.broader, b.uri))
            graph.add((b.uri, SKOS.narrower, uri))
        for n in concept.narrower:
            graph.add((uri, SKOS.narrower, n.uri))
            graph.add((n.uri, SKOS.broader, uri))

        for kid in concept.narrower:
            self.instantiate_rec(kid, graph)

        if concept.broader is None or len(concept.broader) == 0:
            graph.add((uri, SKOS.topConceptOf, self.scheme.scheme_uri))

    @staticmethod
    def collect_and_add_notes(notes, concept):
        if notes:
            for n in notes.split('\n'):
                current_note = ''
                if n != 'nan':
                    if n.startswith('@phrase:'):
                        n = n[7:]
                        concept.add_note('phrase', n)
                    elif n.startswith('@'):
                        if current_note:
                            concept.add_note(current_note)
                        current_note = ''
                    else:
                        current_note += n
            if current_note:
                concept.add_note(current_note)

    def add_properties(self, graph, concept, uri):
        if concept.props:
            for (prop, value) in concept.props:
                lang_sep = value.find('@')
                if lang_sep > -1:
                    lit_val = value[:lang_sep]
                    lang = value[lang_sep+1:]
                else:
                    lit_val = value
                    lang = ''
                if lit_val:
                    lit_val = ProcessUtils.trim(lit_val)
                    literal = Literal(lit_val, lang=lang)
                    prop = self.adjust_namespace(prop, graph)
                    my_property = URIRef(prop)
                    graph.add((uri, my_property, literal))

    @staticmethod
    def adjust_namespace(prop, graph):
        if prop.startswith('skos:'):
            prop = Namespace(SKOS) + prop[5:]
        elif prop.startswith('rdf'):
            prop = Namespace(RDF) + prop[4:]
        elif prop.startswith('rdfs'):
            prop = Namespace(RDFS) + prop[5:]
        return prop




