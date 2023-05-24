from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


# Identify concepts without a topConcept
class OrphanConceptIdentifier(StructureTestInterface):

    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts without any associative or " \
                                                           "hierarchical relationships."
        return message

    @property
    def query(self):
        return """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                SELECT ?concept
                WHERE {
                  ?concept a skos:Concept .
                           
                    FILTER NOT EXISTS {
                        ?concept skos:narrower|skos:broader|skos:related|skos:topConceptOf|skos:hasTopConcept ?relatedConcept .
                    }
                } 
                """






