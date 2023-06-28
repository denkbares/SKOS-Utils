from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SolelyTransitivelyRelatedConceptsChecker(StructureTestInterfaceNavigate):
    """
    Check if every concept has a conceptScheme.
    """

    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts explicitly related by skos:broaderTransitive " \
                                                           "and/or skos:narrowerTransitive."
        return message

    def find_concepts(self, graph):

        bad_concepts_list = []

        for concept in graph.subjects(RDF.type, SKOS.Concept):
        # for concept in graph.triples((None, RDF.type, SKOS.Concept)):
            if any(((concept, SKOS.broaderTransitive, None) in graph,
                    (concept, SKOS.narrowerTransitive, None) in graph)):
                bad_concepts_list.append(concept)

        return bad_concepts_list
