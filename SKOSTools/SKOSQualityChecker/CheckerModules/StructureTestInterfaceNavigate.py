from abc import abstractmethod

from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class StructureTestInterfaceNavigate(StructureTestInterface):
    @abstractmethod
    def find_concepts(self, graph):
        """Define me, so that a list of URIs is returned."""

    def execute(self, graph):
        concepts_result = self.find_concepts(graph)
        return self.create_result(concepts_results=concepts_result)