from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class OrphanConceptChecker(StructureTestInterfaceNavigate):
    """
    Identify concepts without a topConcept.
    """

    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts without any associative or " \
                                                           "hierarchical relationships."
        return message

    def find_concepts(self, graph):
        bad_concept_list = []
        for concept, p, o in graph.triples((None, RDF.type, SKOS.Concept)):
            if not any(((concept, SKOS.related, None) in graph,
                        (None, SKOS.related, concept) in graph,
                        (concept, SKOS.broader, None) in graph,
                        (None, SKOS.broader, concept) in graph,
                        (concept, SKOS.narrower, None) in graph,
                        (None, SKOS.narrower, concept) in graph,
                        (concept, SKOS.hasTopConcept, None) in graph,
                        (None, SKOS.hasTopConcept, concept) in graph,
                        (concept, SKOS.topConceptOf, None) in graph,
                        (None, SKOS.topConceptOf, concept) in graph)):
                bad_concept_list.append(concept)
        return bad_concept_list
