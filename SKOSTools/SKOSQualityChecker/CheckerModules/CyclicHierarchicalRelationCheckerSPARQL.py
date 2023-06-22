from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceSPARQL import StructureTestInterfaceSPARQL


class CyclicHierarchicalRelationCheckerSPARQL(StructureTestInterfaceSPARQL):
    """
    Check whether there is a hierarchical relation.
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

