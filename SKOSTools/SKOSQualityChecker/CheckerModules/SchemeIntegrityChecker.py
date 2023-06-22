from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SchemeIntegrityChecker(StructureTestInterfaceNavigate):
    """
    Check if every concept has a conceptScheme.
    """
    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts without a conceptScheme."
        return message

    def find_concepts(self, graph):
        bad_concepts_list = []

        for concept, p, o in graph.triples((None, RDF.type, SKOS.Concept)):
            if (concept, SKOS.inScheme, None) not in graph:
                bad_concepts_list.append(concept)

        return bad_concepts_list

