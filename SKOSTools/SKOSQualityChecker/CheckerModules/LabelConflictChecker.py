from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class LabelConflictChecker(StructureTestInterfaceNavigate):
    """
    Check whether there are multiple concepts with the same prefLabels in the same concept scheme.
    Considers prefLabels defined in standard SKOS and SKOS-XL.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        if len(result_df) > 0:
            return "There are " + str(len(result_df)) + " concepts with label conflicts."
        return ""

    def find_concepts(self, graph):
        bad_concepts_list = []
        labels = []
        for concept, p, o in graph.triples((None, RDF.type, SKOS.Concept)):
            for label in self.all_pref_labels(concept, graph):
                labels.append([label, concept])

        for concept, p, o in graph.triples((None, RDF.type, SKOS.Concept)):
            if self.conflict_labels(labels, self.all_pref_labels(concept, graph), concept):
                bad_concepts_list.append(concept)
        return bad_concepts_list

    @staticmethod
    def conflict_labels(labels, concept_labels, concept):
        for label1 in labels:
            for concept_label in concept_labels:
                if label1[0].value == concept_label.value and label1[1] != concept:
                    return True
        return False
