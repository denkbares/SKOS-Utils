from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


# Identify concepts without a topConcept
class TopConceptIdentifier(StructureTestInterface):

    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " top concepts in the given graph."
        return message

    @property
    def query(self):
        return """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                SELECT DISTINCT ?concept
                WHERE {
                    {
                          ?concept a skos:Concept ;
                                        skos:inScheme ?scheme .
                          FILTER NOT EXISTS {?concept skos:broader ?parent}
                        # Check, if a concept has the "topConcept" as narrower
                          FILTER NOT EXISTS {?someParentConcept skos:narrower ?concept}
                    }
                    UNION
                    {
                        # Concepts with "topConceptOf" property
                        ?concept a skos:Concept ;
                                    skos:inScheme ?scheme ;
                                    skos:topConceptOf ?someConcept .
                    }
                }
                GROUP BY ?concept

                """

