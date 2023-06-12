from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class SinglePrefLabelChecker(StructureTestInterface):
    """
    Check whether every concept has at most one prefLabel for each language.
    """
    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        if len(result_df) > 0:
            return "There are " + str(len(result_df)) + " concepts with multiple prefLabels for a single language."
        return ""

    @property
    def query(self):
        return """
            SELECT DISTINCT ?concept
            WHERE { ?concept skos:prefLabel ?label1, ?label2 .
                    FILTER (?label1 != ?label2)
                    FILTER (lang(?label1) = lang(?label2))
            }
            GROUP BY ?concept
            """

