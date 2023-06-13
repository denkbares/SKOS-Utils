from rdflib import SKOS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SinglePrefLabelChecker(StructureTestInterfaceNavigate):
    """
    Check whether every concept has at most one prefLabel for each language.
    Considers prefLabels defined in standard SKOS and SKOS-XL.
    """
    @property
    def status(self):
        return "Error"

    def message(self, result):
        if len(result) > 0:
            return "There are " + str(len(result)) + " concepts with multiple prefLabels for a single language."
        return ""

    def find_concepts(self, graph):
        #obj = graph.ojects(None, SKOS.prefLabel, None)
        # todo navigate graph and find deficiencies
        return []
