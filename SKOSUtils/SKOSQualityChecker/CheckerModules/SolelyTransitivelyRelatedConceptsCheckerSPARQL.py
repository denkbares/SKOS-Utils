from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL
from SKOSUtils.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class SolelyTransitivelyRelatedConceptsCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Check if two concepts are related by skos:broaderTransitive and/or skos:narrowerTransitive.
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

