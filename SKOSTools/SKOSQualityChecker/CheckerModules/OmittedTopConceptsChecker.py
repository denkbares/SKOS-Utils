from rdflib import RDF, SKOS, RDFS
import itertools

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class OmittedTopConceptsChecker(StructureTestInterfaceNavigate):
    """
    Identify top concepts.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts not connected to any top concept."
        return message

    def find_concepts(self, graph):
        # TODO: Implement method
        return

        # stack = []
        # bad_concepts_list = []
        # connected_concepts = []
        # top_concepts = []
        #
        # for concept in graph.subjects(predicate=SKOS.topConceptOf):
        #     top_concepts.append(concept)
        # for o in graph.objects(predicate=SKOS.hasTopConcept):
        #     top_concepts.append(o)
        #
        # # Perform a deep search starting from top concepts
        # while stack:
        #     concept = stack.pop()
        #
        #     connected_concepts.append(concept)
        #     narrower_concepts1 = set(graph.subjects(predicate=SKOS.broader, object=concept))
        #     narrower_concepts2 = set(graph.objects(subject=concept, predicate=SKOS.narrower))
        #     narrower_concepts = set(itertools.chain(narrower_concepts1, narrower_concepts2))
        #     for narrower_concept in narrower_concepts:
        #         if narrower_concept in connected_concepts:
        #             bad_concepts_list.append(concept)
        #         else:
        #             stack.append(narrower_concept)

        # return bad_concepts_list

