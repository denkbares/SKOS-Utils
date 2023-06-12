from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class LabelConflictChecker(StructureTestInterface):
    """
    Check whether narrower and broader concepts of a concept are in the same conceptScheme.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with label conflicts."
        return message

    @property
    def query(self):
        return """
                SELECT ?concept1
                WHERE {
                  ?concept1 a skos:Concept ;
                            skos:prefLabel ?label1 .
                  ?concept2 a skos:Concept ;
                            skos:prefLabel ?label2 .
                  
                  FILTER (?label1 = ?label2 && ?concept1 != ?concept2)
                }
        """

