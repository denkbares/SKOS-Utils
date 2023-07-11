from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SchemeIntegrityChecker(StructureTestInterfaceNavigate):
    """
    Check if every concept has a conceptScheme.
    Implements a part of the definition as described in:
    Allemang, D., Hendler, J. A., & Gandon, F. (2020). Semantic web for the working ontologist. ACM Press.
    """
    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts without a conceptScheme."
        return message

    def find_concepts(self, graph):
        bad_concepts_list = []

        for concept in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
            if (concept, SKOS.inScheme, None) not in graph:
                bad_concepts_list.append(concept)

        return bad_concepts_list

