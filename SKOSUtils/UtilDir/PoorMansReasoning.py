import logging

from rdflib import RDFS, SKOS, RDF


class PoorMansReasoning:

    def infer(self, g, max_iterations=100):
        """
        This method adds very simple and direct derivations of
        skos:Concept, skos:broader, skos:narrower, skos:topConceptOf, etc.
        to the specified graph, e.g., a direct subClassOf/subPropertyOf.
        """
        new_triple_added = True
        current_iteration = 0
        while new_triple_added and current_iteration < max_iterations:
            new_triple_added = False
            # add simple subclass properties
            for kid_class, p, o in g.triples((None, RDFS.subClassOf, SKOS.Concept)):
                for concept, p2, o2 in g.triples((None, RDF.type, kid_class)):
                    added = self.add(g, (concept, RDF.type, SKOS.Concept))
                    new_triple_added = new_triple_added or added
            for kid_class, p, o in g.triples((None, RDFS.subClassOf, SKOS.ConceptScheme)):
                for concept, p2, o2 in g.triples((None, RDF.type, kid_class)):
                    added = self.add(g, (concept, RDF.type, SKOS.ConceptScheme))
                    new_triple_added = new_triple_added or added
            # add simple subproperty properties
            for kid_prop, p, o in g.triples((None, RDFS.subPropertyOf, SKOS.broader)):
                for c1, p2, c2 in g.triples((None, kid_prop, None)):
                    added = self.add(g, (c1, SKOS.broader, c2))
                    new_triple_added = new_triple_added or added
            for kid_prop, p, o in g.triples((None, RDFS.subPropertyOf, SKOS.narrower)):
                for c1, p2, c2 in g.triples((None, kid_prop, None)):
                    added = self.add(g, (c1, SKOS.narrower, c2))
                    new_triple_added = new_triple_added or added
            # add the inverse properties to the graph
            for concept, p, o in g.triples((None, RDF.type, SKOS.Concept)):
                for c1, p2, broader in g.triples((concept, SKOS.broader, None)):
                    added = self.add(g, (broader, SKOS.narrower, concept))
                    new_triple_added = new_triple_added or added
                for c2, p2, narrower in g.triples((concept, SKOS.narrower, None)):
                    added = self.add(g, (narrower, SKOS.broader, concept))
                    new_triple_added = new_triple_added or added
            for concept, p, scheme in g.triples((None, SKOS.topConceptOf, None)):
                added = self.add(g, (scheme, SKOS.hasTopConcept, concept))
                new_triple_added = new_triple_added or added
            for scheme, p, concept in g.triples((None, SKOS.hasTopConcept, None)):
                added = self.add(g, (concept, SKOS.topConceptOf, scheme))
                new_triple_added = new_triple_added or added
            # we iterate until no new triples have been derived
            current_iteration += 1
        if current_iteration >= max_iterations:
            logging.WARNING('Maximum iterations for PoorMansReasoning exceeded.')
        return g

    @staticmethod
    def add(g, triple):
        if triple not in g:
            g.add(triple)
            return True
        return False
