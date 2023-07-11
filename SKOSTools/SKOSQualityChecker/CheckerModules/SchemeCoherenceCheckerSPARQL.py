from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class SchemeCoherenceCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Check if narrower and broader concepts of a concept are in the same conceptScheme.
    Implements a part of the definition as described in:
    D. Allemang, J. A. Hendler, & F. Gandon, Semantic web for the working ontologist (2020). ACM Press.
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
            
    
            
        """

