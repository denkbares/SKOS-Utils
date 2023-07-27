import itertools

from rdflib import RDF, SKOS, RDFS, Graph

from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate

class CyclicHierarchicalRelationChecker(StructureTestInterfaceNavigate):
    """
    Traverses all SKOS concept schemes and traverses the narrower/broader relations
    in order to find a directed cycle.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
    """
    def __init__(self):
        super().__init__()
        self.visited_concepts = set()
        self.graph = None
        self.cyclic_relation_concepts = []

    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with cyclic hierarchical relations."
        return message

    def find_concepts(self, graph):
        self.cyclic_relation_concepts = []
        self.graph = graph
        for scheme, p, o in graph.triples((None, RDF.type, SKOS.ConceptScheme)):
            self.visited_concepts = set()
            for concept, p, o2 in graph.triples((None, SKOS.topConceptOf, scheme)):
                self.depth_first_search(concept, [scheme])
        return self.cyclic_relation_concepts

    def depth_first_search(self, concept, path):
        if concept in self.visited_concepts:
            return
        self.visited_concepts.add(concept)
        path.append(concept)
        for concept, p, narrower_concept in self.graph.triples((concept, SKOS.narrower, None)):
            if narrower_concept in path:
                self.cyclic_relation_concepts.append(narrower_concept)
                self.send_log('Cycle found: ' + str(path) + ' > ' + str(narrower_concept))
            elif narrower_concept in self.visited_concepts:
                return
            else:
                self.depth_first_search(narrower_concept, path.copy())
