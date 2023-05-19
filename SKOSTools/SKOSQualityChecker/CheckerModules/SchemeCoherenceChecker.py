from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


# Check if narrower and broader concepts of a concept are in the same conceptScheme

class SchemeCoherenceChecker(StructureTestInterface):

    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with violated scheme coherence."
        return message

    @property
    def query(self):
        return """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
            SELECT ?concept 
            WHERE {
                ?concept a skos:Concept .
                # FILTER NOT EXISTS {
                    ?concept skos:inScheme/rdf:type skos:ConceptScheme .
                # }
                # OPTIONAL {
                #     ?concept skos:narrower|skos:broader ?relatedConcept .
                #     ?relatedConcept skos:inScheme ?scheme
                #     FILTER(?scheme = ?concept/skos:inScheme)
                # }
                # FILTER(?scheme = ?concept/skos:inScheme)
    
            }
            GROUP BY ?concept
        """

