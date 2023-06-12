from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class IncompleteLanguageCoverageChecker(StructureTestInterface):

    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            # TODO: Specify missing prefLabel languages
            message = "There are " + str(len(result_df)) + " concepts with incomplete language coverage."
            # message = "Missing prefLabel languages: "
        return message

    @property
    def query(self):
        # Check language tags against a list of all language used in the graph.
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

