import uuid

from rdflib import URIRef, RDF, Literal, Graph
from rdflib.namespace import SKOS, Namespace


class Generic2SKOS:
    def __init__(self, namespace, scheme_name, bindings={}, default_language='de'):
        self.default_language = default_language
        self.scheme_name = scheme_name
        self.namespace = namespace
        self.scheme = None
        self.created_concepts = {}
        self.bindings = bindings

    def create_scheme_uri(self, graph):
        schemename = self.scheme_name
        su = URIRef(self.namespace + schemename)
        graph.add((su, RDF.type, SKOS.ConceptScheme))
        graph.add((su, SKOS.prefLabel, Literal(schemename, self.default_language)))
        graph.add((su, SKOS.prefLabel, Literal(schemename)))
        return su

    def add_binding(self, abbr, uri):
        self.bindings[uri] = abbr

    def to_rdf(self, scheme, out_filename):
        self.created_concepts = {}
        graph = Graph()
        skos_ns = Namespace(SKOS)
        graph.bind("skos", skos_ns)
        scheme.scheme_uri = self.create_scheme_uri(graph, scheme)
        for buri, babbr in self.bindings.items():
            graph.bind(babbr, buri)
        for tc in scheme.top_concepts:
            self.instantiate_rec(tc, graph)
        graph.serialize(format='turtle', destination=out_filename)

    def create_scheme_uri(self, graph, scheme):
        schemename = scheme.name
        su = URIRef(self.namespace + schemename)
        graph.add((su, RDF.type, SKOS.ConceptScheme))
        graph.add((su, SKOS.prefLabel, Literal(schemename, self.default_language)))
        graph.add((su, SKOS.prefLabel, Literal(schemename)))
        return su

    def instantiate_rec(self, concept, graph):
        if concept.uri:
            uri = concept.uri
        else:
            uri = URIRef(uuid.uuid4())
        self.created_concepts[uri] = uri
        graph.add((uri, RDF.type, SKOS.Concept))
        graph.add((uri, SKOS.prefLabel, Literal(concept.name, lang=self.default_language)))
        graph.add((uri, SKOS.prefLabel, Literal(concept.name)))
        if concept.notes:
            for note in concept.notes:
                graph.add((uri, SKOS.note, Literal(note)))
        graph.add((uri, SKOS.inScheme, self.scheme.scheme_uri))
        for b in concept.broader:
            graph.add((uri, SKOS.broader, b.uri))
        for n in concept.narrower:
            graph.add((uri, SKOS.narrower, n.uri))

        for kid in concept.narrower:
            self.instantiate_rec(kid, graph)

        if concept.broader is None or len(concept.broader) == 0:
            graph.add((uri, SKOS.topConceptOf, self.scheme.scheme_uri))
