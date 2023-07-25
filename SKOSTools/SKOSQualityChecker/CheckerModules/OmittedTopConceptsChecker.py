from rdflib import RDF, SKOS, RDFS
from itertools import chain
from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class OmittedTopConceptsChecker(StructureTestInterfaceNavigate):
    """
    Identify all SKOS concepts that are not connected to any top concept in the concept scheme.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
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

        for concept in graph.subjects(predicate=SKOS.topConceptOf):
            top_concepts.add(concept)
        for o in graph.objects(predicate=SKOS.hasTopConcept):
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
        for concept in graph.subjects(predicate=SKOS.inScheme):
            if concept not in connected_concepts:
                unconnected_concepts.append(concept)

        return unconnected_concepts
