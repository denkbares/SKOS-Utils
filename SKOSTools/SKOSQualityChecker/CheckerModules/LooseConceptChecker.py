from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class LooseConceptChecker(StructureTestInterfaceNavigate):
    """
    Identify concepts without a topConcept.
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
        # TODO Write utility function "get_all_top_concepts()"?
        top_concepts = []
        unconnected_concepts = []
        connected_concepts = []

        for concept, p, o in graph.triples((None, SKOS.topConceptOf, None)):
            top_concepts.append(concept)
        for concept, p, o in graph.triples((None, SKOS.hasTopConcept, None)):
            top_concepts.append(o)

            # Perform a deep search starting from top concepts
            stack = list(top_concepts)
            while stack:
                concept = stack.pop()
                connected_concepts.append(concept)
                narrower_concepts = graph.subjects(predicate=SKOS.broader, object=concept) \
                                    and graph.objects(subject=concept, predicate=SKOS.narrower)
                stack.extend(narrower_concepts)

            # Find unconnected concepts
            for conc in graph.subjects(predicate=SKOS.inScheme):
                if conc not in connected_concepts:
                    unconnected_concepts.append(conc)

        return unconnected_concepts
