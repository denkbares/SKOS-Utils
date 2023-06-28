from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class SchemeCoherenceCheckerSPARQL(StructureTestInterfaceSPARQL):
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

    @property
    def query(self):
        # TODO: Write SPARQL Query
        return """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
            
        """

