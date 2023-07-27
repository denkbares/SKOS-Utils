from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class SchemeIntegrityCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Check if every concept has a conceptScheme.
    Implements a part of the definition as described in:
    D. Allemang, J. A. Hendler, & F. Gandon, Semantic web for the working ontologist (2020). ACM Press.
    """
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

