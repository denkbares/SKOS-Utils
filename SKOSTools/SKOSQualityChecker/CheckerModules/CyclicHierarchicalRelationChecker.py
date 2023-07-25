import itertools

from rdflib import RDF, SKOS, RDFS, Graph

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


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
        self.full_graph = None
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
        self.full_graph = self.make_full_graph(graph)
        self.cyclic_relation_concepts = []

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
        for concept, p, narrower_concept in self.full_graph.triples((concept, SKOS.narrower, None)):
            if narrower_concept in path:
                self.cyclic_relation_concepts.append(narrower_concept)
                self.send_log('Cycle found: ' + str(path) + ' > ' + str(narrower_concept))
            elif narrower_concept in self.visited_concepts:
                return
            else:
                self.depth_first_search(narrower_concept, path.copy())

    @staticmethod
    def make_full_graph(original_graph):
        g = Graph()
        for concept, p, o in original_graph.triples((None, RDF.type, SKOS.Concept)):
            for c1, p2, broader in original_graph.triples((concept, SKOS.broader, None)):
                g.add((concept, SKOS.broader, broader))
                g.add((broader, SKOS.narrower, concept))
            for c2, p2, narrower in original_graph.triples((concept, SKOS.narrower, None)):
                g.add((concept, SKOS.narrower, narrower))
                g.add((narrower, SKOS.broader, concept))
        for concept, p, scheme in original_graph.triples((None, SKOS.topConceptOf, None)):
            g.add((concept, SKOS.topConceptOf, scheme))
            g.add((scheme, SKOS.hasTopConcept, concept))
        for scheme, p, concept in original_graph.triples((None, SKOS.hasTopConcept, None)):
            g.add((concept, SKOS.topConceptOf, scheme))
            g.add((scheme, SKOS.hasTopConcept, concept))
        return g
