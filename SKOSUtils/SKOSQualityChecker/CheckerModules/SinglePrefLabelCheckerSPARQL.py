from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class SinglePrefLabelCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Check whether every concept has at most one prefLabel for each language.
    Considers prefLabels defined in standard SKOS and SKOS-XL.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
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
            PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
            SELECT DISTINCT ?concept
            WHERE { { ?concept skos:prefLabel ?label1, ?label2 . }
                    UNION
                    { ?concept skosxl:prefLabel/skosxl:literalForm ?label3, ?label4 . }
                    FILTER ((?label1 != ?label2 && lang(?label1) = lang(?label2)) ||
                            (?label3 != ?label4 && lang(?label3) = lang(?label4)))
            }
            GROUP BY ?concept
            """
