from abc import abstractmethod

import pandas as pd

from SKOSTools.SKOSQualityChecker.CheckerModules.Structure_Test_Interface import StructureTestInterface


class StructureTestInterfaceSPARQL(StructureTestInterface):
    pass

    @property
    @abstractmethod
    def query(self):
        """Define me: we expect a result with one column named 'concept'"""
        pass

    def execute(self, graph):
        results_query = graph.query(self.query)
        concepts_result = self.to_list(results_query)
        results_df = self.create_result(concepts_results=concepts_result)
        return results_df

    def to_list(self, results_query):
        l = []
        for row in results_query:
            l.append(row.concept)
        return l
