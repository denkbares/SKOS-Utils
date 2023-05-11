from abc import ABC, abstractmethod
import pandas as pd


class StructureTestInterface(ABC):
    @property
    @abstractmethod
    def status(self):
        """Define me"""
        pass

    @abstractmethod
    def message(self, result_df):
        pass

    @property
    @abstractmethod
    def query(self):
        pass

    def execute(self, graph):
        results_query = graph.query(self.query)
        results_df = pd.DataFrame(results_query, columns=['Concept'])
        # Add other columns ("Status", "CheckName", "Msg", "URIs")
        results_df.insert(0, 'Status', self.status)
        results_df.insert(0, 'CheckName', self.__class__.__name__)
        results_df.insert(2, 'Message', self.message(results_df))

        return results_df
