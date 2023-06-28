from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class InvalidLanguageTagChecker(StructureTestInterfaceNavigate):
    """
    Checks language tags against a list of all valid language tags defined in RFC3066.
    """
    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with invalid language tags."
        return message

    def find_concepts(self, graph):
        # TODO: Check language tags against a list of all language tags defined in RFC3066.
        return

