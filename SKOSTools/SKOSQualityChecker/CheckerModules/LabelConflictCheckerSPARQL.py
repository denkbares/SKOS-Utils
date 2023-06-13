from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class LabelConflictCheckerSPARQL(StructureTestInterfaceSPARQL):
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
                SELECT ?concept
                WHERE {
                  ?concept a skos:Concept ;
                            skos:prefLabel ?label1 .
                  ?concept2 a skos:Concept ;
                            skos:prefLabel ?label2 .
                  
                  FILTER (?label1 = ?label2 && ?concept != ?concept2)
                }
        """

