from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


# Check if every concept has a conceptScheme
class SchemeIntegrityCheckerSPARQL(StructureTestInterfaceSPARQL):

    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts without a conceptScheme."
        return message

    @property
    def query(self):
        return """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
            SELECT ?concept
            WHERE {
                ?concept a skos:Concept .
                FILTER NOT EXISTS {
                    ?concept skos:inScheme/rdf:type skos:ConceptScheme .
                }
            }
            GROUP BY ?concept
            """

