from rdflib import RDF, SKOS, RDFS

from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SchemeIntegrityChecker(StructureTestInterfaceNavigate):
    """
    Lists all SKOS concepts that are not explicitly linked to a concept scheme.
    Implements a part of the definition as described in:
    D. Allemang, J. A. Hendler, & F. Gandon, Semantic web for the working ontologist (2020). ACM Press.
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

