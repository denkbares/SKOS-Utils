from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class LabelConflictChecker(StructureTestInterfaceNavigate):
    """
    Check whether there are multiple concepts with the same prefLabels in the same concept scheme.
    Considers prefLabels defined in standard SKOS and SKOS-XL.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        if len(result_df) > 0:
            return "There are " + str(len(result_df)) + " concepts with label conflicts."
        return ""

    # def find_concepts(self, graph):
    #     bad_concepts_list = []
    #     labels = []
    #     concepts = list(graph.subjects(predicate=RDF.type, object=SKOS.Concept))
    #     for concept in concepts:
    #         for label in self.all_pref_labels(concept, graph):
    #             labels.append([label, concept])
    #
    #     for concept in concepts:
    #         if self.conflict_labels(labels, self.all_pref_labels(concept, graph), concept):
    #             bad_concepts_list.append(concept)
    #     return bad_concepts_list
    #
    # @staticmethod
    # def conflict_labels(labels, concept_labels, concept):
    #     for label1 in labels:
    #         for concept_label in concept_labels:
    #             if label1[0].value == concept_label.value and label1[1] != concept:
    #                 return True
    #     return False

    def find_concepts(self, graph):
        bad_concepts_list = []
        labels = {}
        concepts = list(graph.subjects(predicate=RDF.type, object=SKOS.Concept))

        for concept in concepts:
            concept_labels = self.all_pref_labels(concept, graph)
            for label in concept_labels:
                labels[label.value] = labels.get(label.value, []) + [concept]

        for concept in concepts:
            concept_labels = self.all_pref_labels(concept, graph)
            if self.conflict_labels(labels, concept_labels, concept):
                bad_concepts_list.append(concept)

        return bad_concepts_list

    @staticmethod
    def conflict_labels(labels, concept_labels, concept):
        for label in concept_labels:
            if label.value in labels:
                for other_concept in labels[label.value]:
                    if other_concept != concept:
                        return True
        return False
