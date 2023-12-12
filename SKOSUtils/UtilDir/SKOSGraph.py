import uuid

from rdflib import namespace, Graph, SKOS, RDF, URIRef, RDFS


class SKOSGraph:
    TOP_CONCEPT_OF = URIRef(namespace.SKOS + "topConceptOf")
    CONCEPT_SCHEME = URIRef(namespace.SKOS + "ConceptScheme")
    CONCEPT = URIRef(namespace.SKOS + "Concept")
    BROADER = URIRef(namespace.SKOS + "broader")
    NARROWER = URIRef(namespace.SKOS + "narrower")
    PREF_LABEL = URIRef(namespace.SKOS + 'prefLabel')
    NOTE = URIRef(namespace.SKOS + 'note')

    def __init__(self, rdf_filename, namespaces={}, poor_man_reasoning=False):
        self.g = Graph()
        self.namespaces = namespaces
        self.g.parse(rdf_filename, format='turtle')
        if poor_man_reasoning:
            self.g = self.poor_man_reasoning(self.g)
        self.generated_uuid = []

    def generate_uuid(self):
        short_uuid = str(uuid.uuid4())[:8]
        while short_uuid not in self.generated_uuid:
            short_uuid = str(uuid.uuid4())[:8]
        return short_uuid

    def top_concepts(self, scheme_uri):
        return self.g.subjects(self.TOP_CONCEPT_OF, scheme_uri)

    def pref_label(self, uri, lang):
        literals = list(self.g.objects(uri, SKOS.prefLabel))
        for lit in literals:
            if lit.language == lang:
                return lit
        if literals and len(literals) > 0:
                return str(literals[0])
        return ""

    def hidden_label(self, uri, lang):
        literals = list(self.g.objects(uri, SKOS.hiddenLabel))
        for lit in literals:
            if lit.language == lang:
                return lit
        if literals and len(literals) > 0:
                return str(literals[0])
        return ""

    def alt_labels(self, uri):
        pref_labels = list(self.g.objects(uri, SKOS.prefLabel))
        labels = []
        for literal in self.g.objects(uri, SKOS.altLabel):
            if literal not in pref_labels:
                labels.append(str(literal))
        return labels

    def alt_label(self, uri, lang):
        literals = self.g.objects(uri, SKOS.altLabel)
        for lit in literals:
            if lit.language == lang:
                return lit
        return literals

    def concept_schemes(self):
        return self.g.subjects(RDF.type, self.CONCEPT_SCHEME)

    def all_concepts(self):
        return self.g.subjects(RDF.type, self.CONCEPT)

    def narrower(self, uri):
        return self.g.objects(uri, self.NARROWER)

    def broader(self, uri):
        return self.g.objects(uri, self.BROADER)

    def note(self, uri):
        return self.g.objects(uri, self.NOTE)

    def note_with_prefix(self, uri, prefix):
        for n in self.note(uri):
            if str(n).startswith(prefix):
                return str(n)
        return None

    def order(self, uri):
        for note in self.note(uri):
            n = str(note)
            if n.startswith('@order:'):
                return int(n[7:].strip())
        return 1

    def plain_notes(self, uri):
        note = ''
        referred_objects = self.note(uri)
        for ref in referred_objects:
            note = note + str(ref.value)
            note = note + '\n'
        return note[:len(note) - 1]

    def trim_notes(self, uri, remove_with_prefixes=None):
        """Removes all note property triples pointing the given List of 'remove_with_prefixes'"""
        if remove_with_prefixes:
            referred_objects = self.note(uri)
            for ref in referred_objects:
                note = str(ref.value)
                for prefix in remove_with_prefixes:
                    if note.startswith(prefix):
                        self.g.remove((uri, self.NOTE, ref))

    def str_abbr(self, uri):
        uri_s = str(uri)
        for ns in self.namespaces.keys():
            if uri_s.startswith(ns):
                subst = self.namespaces[ns]
                return subst + ':' + uri_s[len(ns):]
        return uri_s

    @staticmethod
    def poor_man_reasoning(g):
        # add simple subclass properties
        for kid_class, p, o in g.triples((None, RDFS.subClassOf, SKOS.Concept)):
            for concept, p2, o2 in g.triples((None, RDF.type, kid_class)):
                g.add((concept, RDF.type, SKOS.Concept))
        # add simple subproperty properties
        for kid_prop, p, o in g.triples((None, RDFS.subPropertyOf, SKOS.broader)):
            for c1, p2, c2 in g.triples((None, kid_prop, None)):
                g.add((c1, SKOS.broader, c2))
        for kid_prop, p, o in g.triples((None, RDFS.subPropertyOf, SKOS.narrower)):
            for c1, p2, c2 in g.triples((None, kid_prop, None)):
                g.add((c1, SKOS.narrower, c2))
        # add the inverse properties to the graph
        for concept, p, o in g.triples((None, RDF.type, SKOS.Concept)):
            for c1, p2, broader in g.triples((concept, SKOS.broader, None)):
                g.add((broader, SKOS.narrower, concept))
            for c2, p2, narrower in g.triples((concept, SKOS.narrower, None)):
                g.add((narrower, SKOS.broader, concept))
        for concept, p, scheme in g.triples((None, SKOS.topConceptOf, None)):
            g.add((scheme, SKOS.hasTopConcept, concept))
        for scheme, p, concept in g.triples((None, SKOS.hasTopConcept, None)):
            g.add((concept, SKOS.topConceptOf, scheme))
        return g
