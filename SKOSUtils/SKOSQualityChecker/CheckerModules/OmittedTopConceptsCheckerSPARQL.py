from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class OmittedTopConceptsCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Identify concepts that are not connected to any top concept.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
    """

    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts not connected to any topConcept in the given " \
                                                           "graph."
        return message

    @property
    def query(self):
        # TODO: Add concepts, that are connected to a topConcept with "narrower"
        return """
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
                SELECT DISTINCT ?concept
                WHERE {
                  ?concept a skos:Concept ;
                           skos:inScheme ?scheme .
    
                  FILTER NOT EXISTS {
                    ?topConcept a skos:Concept ;
                                skos:inScheme ?scheme ;
                                skos:topConceptOf ?someConcept .
                    ?concept skos:broader* ?topConcept .
                  }
                } 
                GROUP BY ?concept
    
                """






