from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


# Identify concepts without a topConcept
class TopConceptHavingBroaderConceptsCheckerSPARQL(StructureTestInterfaceSPARQL):

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

