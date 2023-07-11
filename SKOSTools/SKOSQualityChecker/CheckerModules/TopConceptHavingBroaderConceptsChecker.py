from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class TopConceptHavingBroaderConceptsChecker(StructureTestInterfaceNavigate):
    """
    Check if Top Concepts have broader concepts.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
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
        # TODO Write utility function "get_all_top_concepts()"?
        top_concept_list = []
        bad_concepts_list = []
        for concept in graph.subjects(predicate=SKOS.topConceptOf):
            top_concept_list.append(concept)
        for o in graph.objects(predicate=SKOS.hasTopConcept):
            top_concept_list.append(o)

        for top_concept in top_concept_list:
            if (top_concept, SKOS.broader, None) in graph:
                bad_concepts_list.append(top_concept)
        return bad_concepts_list




