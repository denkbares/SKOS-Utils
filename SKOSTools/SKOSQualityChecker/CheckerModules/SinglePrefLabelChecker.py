from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


# Check if every concept has only 1 prefLabel for each language
class SinglePrefLabelChecker(StructureTestInterface):

    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with multiple PrefLabels for a single language."
        return message

    @property
    def query(self):
        return """
            SELECT DISTINCT ?concept
            WHERE {?concept skos:prefLabel ?label1 .
                    ?concept skos:prefLabel ?label2 .
                FILTER (lang (?label1) = lang (?label2))
                FILTER (?label1 != ?label2)
            }
            GROUP BY ?concept
            """

