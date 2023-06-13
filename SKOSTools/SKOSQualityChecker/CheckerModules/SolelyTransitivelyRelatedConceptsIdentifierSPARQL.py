from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL
from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


# Check if every concept has a conceptScheme
class SolelyTransitivelyRelatedConceptsIdentifierSPARQL(StructureTestInterfaceSPARQL):

    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts explicitly related by skos:broaderTransitive " \
                                                           "and/or skos:narrowerTransitive."
        return message

    @property
    def query(self):
        return """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

            SELECT ?concept
            WHERE {
                ?concept a skos:Concept ;
                    skos:broaderTransitive|skos:narrowerTransitive ?anotherConcept.
            }
            GROUP BY ?concept
            """

