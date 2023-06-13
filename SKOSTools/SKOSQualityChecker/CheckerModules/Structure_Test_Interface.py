from abc import ABC, abstractmethod
import pandas as pd


class StructureTestInterface(ABC):
    @property
    @abstractmethod
    def status(self):
        """Define me"""
        pass

    @abstractmethod
    def message(self, datafolder):
        """Define me"""
        pass

    def create_result(self, concepts_results):
        results_df = pd.DataFrame(concepts_results, columns=['Concept'])
        # Add other columns ("Status", "CheckName", "Msg", "URIs")
        results_df.insert(0, 'Status', self.status)
        results_df.insert(0, 'CheckName', self.__class__.__name__)
        results_df.insert(2, 'Message', self.message(results_df))
        return results_df

    def execute(self, graph):
        pass
