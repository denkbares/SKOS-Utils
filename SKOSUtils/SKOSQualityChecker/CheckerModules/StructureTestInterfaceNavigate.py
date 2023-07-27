from abc import abstractmethod

from rdflib import Namespace, URIRef, SKOS

from SKOSUtils.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class StructureTestInterfaceNavigate(StructureTestInterface):
    SKOSXL_NS = Namespace('http://www.w3.org/2008/05/skos-xl#')
    PREF_LABEL_XL = URIRef(SKOSXL_NS + 'prefLabel')
    LITERAL_FORM_XL = URIRef(SKOSXL_NS + 'literalForm')

    def all_pref_labels(self, concept, graph):
        """Returns all prefLabels of a given concept (only standard SKOS)."""
        return list(graph.objects(concept, SKOS.prefLabel, None))

    def all_pref_labels_xl(self, concept, graph):
        """Returns all prefLabels in SKOS-XL of a given concept."""
        all_labels = []
        for s, p, label in graph.triples((concept, self.PREF_LABEL_XL, None)):
            for su, pr, literal in graph.triples((label, self.LITERAL_FORM_XL, None)):
                all_labels.append(literal)
        return all_labels

    @abstractmethod
    def find_concepts(self, graph):
        """Define me, so that a list of bad concept URIs is returned."""

    def execute(self, graph, logging=None):
        if logging:
            self.log = True
        concepts_result = self.find_concepts(graph)
        return self.create_result(concepts_results=concepts_result)
