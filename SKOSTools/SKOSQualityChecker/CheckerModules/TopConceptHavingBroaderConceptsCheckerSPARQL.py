from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class TopConceptHavingBroaderConceptsCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Check if Top Concepts have broader concepts.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
    """
    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " top concepts with broader concepts."
        return message

    @property
    def query(self):
        return """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                # Select all top concepts and filter those with broader concepts
                SELECT DISTINCT ?concept
                WHERE {
                  {
                    ?concept skos:topConceptOf ?scheme .
                  }
                  UNION
                  {
                    ?otherConcept skos:hasTopConcept ?concept .
                  }
                  FILTER EXISTS {?concept skos:broader ?parent}
                }
                """

