import itertools

from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class CyclicHierarchicalRelationChecker(StructureTestInterfaceNavigate):
    """
    Check whether there is a cyclic hierarchical relation.
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
            message = "There are " + str(len(result_df)) + " concepts with cyclic hierarchical relations."
        return message

    def find_concepts(self, graph):
        stack = []
        cyclic_relation_concepts = set()
        connected_concepts = []

        for concept, p, o in graph.triples((None, SKOS.topConceptOf, None)):
            stack.append(concept)
        for concept, p, o in graph.triples((None, SKOS.hasTopConcept, None)):
            stack.append(o)

        # Perform a deep search starting from top concepts
        while stack:
            concept = stack.pop()

            connected_concepts.append(concept)
            narrower_concepts1 = set(graph.subjects(predicate=SKOS.broader, object=concept))
            narrower_concepts2 = set(graph.objects(subject=concept, predicate=SKOS.narrower))
            narrower_concepts = set(itertools.chain(narrower_concepts1, narrower_concepts2))
            for narrower_concept in narrower_concepts:
                if narrower_concept in connected_concepts:
                    cyclic_relation_concepts.add(concept)
                else:
                    stack.append(narrower_concept)

        return cyclic_relation_concepts
