from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class LabelConflictCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Checks whether there are multiple concepts with the same prefLabels in the same concept scheme
    (currently only supports skos:preLabel).
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        if len(result_df) > 0:
            return "There are " + str(len(result_df)) + " concepts with label conflicts."
        return ""

    @property
    def query(self):
        return """
                SELECT DISTINCT ?concept
                WHERE {
                  ?concept a skos:Concept ;
                            skos:prefLabel ?label1 .
                  ?concept2 a skos:Concept ;
                            skos:prefLabel ?label2 .
                  
                  FILTER (?label1 = ?label2 && ?concept != ?concept2)
                }
        """

