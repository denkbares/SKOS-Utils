from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class InvalidLanguageTagChecker(StructureTestInterface):
    """
    Check if narrower and broader concepts of a concept are in the same conceptScheme
    """
    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with invalid language tags."
        return message

    @property
    def query(self):
        # TODO: Check language tags against a list of all language tags defined in RFC3066.
        return """
            
        """

