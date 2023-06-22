from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class TopConceptIdentifier(StructureTestInterfaceNavigate):
    """
    Identify top concepts.
    """
    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " top concepts in the given graph."
        return message

    def find_concepts(self, graph):
        top_concept_list = []
        concepts_without_broader = set()
        narrower_concepts = set()

        for concept, p, o in graph.triples((None, SKOS.topConceptOf, None)):
            top_concept_list.append(concept)
        for concept, p, o in graph.triples((None, SKOS.hasTopConcept, None)):
            top_concept_list.append(o)
        for concept, p, o in graph.triples((None, RDF.type, SKOS.Concept)):
            if (concept, SKOS.broader, None) not in graph:
                concepts_without_broader.add(concept)
            if (None, SKOS.narrower, concept) in graph:
                narrower_concepts.add(concept)

        final_concepts = concepts_without_broader - narrower_concepts

        for c in final_concepts:
            if not top_concept_list.__contains__(c):
                top_concept_list.append(c)

        return top_concept_list
