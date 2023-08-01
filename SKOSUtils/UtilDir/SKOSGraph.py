import uuid

from rdflib import Graph, SKOS, RDF
from rdflib.namespace import NamespaceManager

from SKOSUtils.UtilDir.PoorMansReasoning import PoorMansReasoning


class SKOSGraph:
    def __init__(self, rdf_filename, namespaces={}, poor_man_reasoning=False):
        # standard namespaces
        standard_ns = { 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                        'skos': 'http://www.w3.org/2004/02/skos/core#',
                        'xsd': 'http://www.w3.org/2001/XMLSchema#',
                        'ex':'http://www.example.org/bike'}
        self.g = Graph()
        self.namespaces = namespaces
        for k in standard_ns:
            self.namespaces[k] = standard_ns[k]

        self.namespace_manager = NamespaceManager(self.g)
        self.g.namespace_manager = self.namespace_manager
        for ns in self.namespaces:
            self.g.namespace_manager.bind(ns, self.namespaces[ns])
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
        return self.g.objects(scheme_uri, SKOS.hasTopConcept)

    def pref_label(self, uri, lang):
        literals = list(self.g.objects(uri, SKOS.prefLabel))
        if lang is None:
            return literals
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

    def alt_label(self, uri, lang):
        literals = self.g.objects(uri, SKOS.altLabel)
        for lit in literals:
            if lit.language == lang:
                return lit
        return literals

    def uri_type(self, concept):
        type_list = list(self.g.objects(concept, RDF.type))
        if type_list and len(type_list) > 0:
            return type_list[0]
        return None

    def qstr(self, uri):
        """
        Returns the qualified string of the given uri
        """
        return self.g.namespace_manager.qname(uri)

    def concept_schemes(self):
        return self.g.subjects(RDF.type, SKOS.ConceptScheme)

    def all_concepts(self):
        return self.g.subjects(RDF.type, SKOS.Concept)

    def narrower(self, uri):
        return self.g.objects(uri, SKOS.narrower)

    def broader(self, uri):
        return self.g.objects(uri, SKOS.broader)

    def note(self, uri):
        return self.g.objects(uri, SKOS.note)

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
                        self.g.remove((uri, SKOS.note, ref))

    def str_abbr(self, uri):
        uri_s = str(uri)
        for ns in self.namespaces.keys():
            if uri_s.startswith(ns):
                subst = self.namespaces[ns]
                return subst + ':' + uri_s[len(ns):]
        return uri_s

    @staticmethod
    def poor_man_reasoning(g):
        poo = PoorMansReasoning()
        return poo.infer(g)
