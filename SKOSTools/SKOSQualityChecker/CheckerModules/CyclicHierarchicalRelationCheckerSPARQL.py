from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class CyclicHierarchicalRelationCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Identify cyclic hierarchical relations.
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
            message = "There are " + str(len(result_df)) + " concepts with cyclic hierarchical relations."
        return message

    @property
    def query(self):
        # TODO:
        return """
                
        """

