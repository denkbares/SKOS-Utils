from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class IncompleteLanguageCoverageCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Checks language tags against a list of all language used in the graph.
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
            message = "There are " + str(len(result_df)) + " concepts with incomplete language coverage."
        return message

    @property
    def query(self):
        return """
        
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
                SELECT ?concept
                WHERE {
                    
                        {
                          # Find the concept set of language tags
                            SELECT ?concept (GROUP_CONCAT(DISTINCT ?lang; SEPARATOR="|") AS ?conceptLangs)
                            WHERE {
                                SELECT *
                                    WHERE {
                                        ?concept a skos:Concept ;
                                            skos:prefLabel ?conceptLabel .
                                            BIND  (LANG(?conceptLabel) AS ?lang)
                                    }
                                ORDER BY ASC(STR(?lang))
                            } 
                        GROUP BY ?concept
                        }
                    
                        {
                          # Find the global set of language tags
                          SELECT (GROUP_CONCAT(DISTINCT ?lang; SEPARATOR="|") AS ?globalLangs)
                          WHERE {
                             SELECT (LANG(?label) AS ?lang)
                                WHERE {
                                    ?c a skos:Concept ;
                                        skos:prefLabel ?label .
                                } 
                                ORDER BY ASC(STR(?lang))
                            } 
                        }
                  FILTER (?conceptLangs != ?globalLangs)
                }
                
        """

