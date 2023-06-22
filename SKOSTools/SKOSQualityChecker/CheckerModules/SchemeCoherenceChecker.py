from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SchemeCoherenceChecker(StructureTestInterfaceNavigate):
    """
    Check if narrower and broader concepts of a concept are in the same conceptScheme.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with violated scheme coherence."
        return message

    def find_concepts(self, graph):
        # TODO: Write function
        return

