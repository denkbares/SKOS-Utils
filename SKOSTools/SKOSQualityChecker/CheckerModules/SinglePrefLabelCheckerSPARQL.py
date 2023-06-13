from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class SinglePrefLabelCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Check whether every concept has at most one prefLabel for each language.
    Considers prefLabels defined in standard SKOS and SKOS-XL.
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
            WHERE { { ?concept skos:prefLabel ?label1, ?label2 . }
                    UNION
                    { ?concept skosxl:prefLabel/skosxl:literalForm ?label1, ?label2 . }
                    FILTER (?label1 != ?label2)
                    FILTER (lang(?label1) = lang(?label2))
            }
            GROUP BY ?concept
            """
