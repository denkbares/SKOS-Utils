from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class OrphanConceptCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Identify concepts without any relation to another concept.
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
                    
                    FILTER NOT EXISTS {
                        ?otherRelatedConcept skos:narrower|skos:broader|skos:related|skos:topConceptOf|skos:hasTopConcept ?concept .
                    }
                } 
                """






