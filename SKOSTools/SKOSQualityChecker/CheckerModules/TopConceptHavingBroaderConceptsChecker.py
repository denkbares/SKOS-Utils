from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class TopConceptHavingBroaderConceptsChecker(StructureTestInterfaceNavigate):
    """
    Check if Top Concepts have broader concepts.
    """
    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " top concepts with broader concepts."
        return message

    def find_concepts(self, graph):
        top_concept_list = []
        bad_concepts_list = []
        for concept, p, o in graph.triples((None, SKOS.topConceptOf, None)):
            top_concept_list.append(concept)
        for concept, p, o in graph.triples((None, SKOS.hasTopConcept, None)):
            top_concept_list.append(o)

        for top_concept in top_concept_list:
            if (top_concept, SKOS.broader, None) in graph:
                bad_concepts_list.append(top_concept)
        return bad_concepts_list




