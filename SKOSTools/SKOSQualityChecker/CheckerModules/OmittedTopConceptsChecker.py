from rdflib import RDF, SKOS, RDFS
from itertools import chain
from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class OmittedTopConceptsChecker(StructureTestInterfaceNavigate):
    """
    Identify concepts that are not connected to any top concept.
    """

    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts not connected to any topConcept in the given " \
                                                           "graph."
        return message

    def find_concepts(self, graph):
        # TODO: Write utility function "get_all_top_concepts()"?
        top_concepts = set()
        unconnected_concepts = []
        connected_concepts = set()

        for concept, p, o in graph.triples((None, SKOS.topConceptOf, None)):
            top_concepts.add(concept)
        for concept, p, o in graph.triples((None, SKOS.hasTopConcept, None)):
            top_concepts.add(o)

        # Perform a deep search starting from top concepts
        stack = top_concepts
        while stack:
            concept = stack.pop()
            connected_concepts.add(concept)
            narrower_concepts1 = graph.subjects(predicate=SKOS.broader, object=concept)
            narrower_concepts2 = graph.objects(subject=concept, predicate=SKOS.narrower)
            narrower_concepts = chain(narrower_concepts1, narrower_concepts2)

            for narrower_concept in narrower_concepts:
                if narrower_concept not in connected_concepts:
                    stack.add(narrower_concept)

        # Find unconnected concepts
        for conc in graph.subjects(predicate=SKOS.inScheme):
            if conc not in connected_concepts:
                unconnected_concepts.append(conc)

        return unconnected_concepts
