from rdflib import RDF, SKOS, RDFS

from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SolelyTransitivelyRelatedConceptsChecker(StructureTestInterfaceNavigate):
    """
    Check whether two SKOS concepts are related by skos:broaderTransitive and/or
    skos:narrowerTransitive properties.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
    """

    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts explicitly related by skos:broaderTransitive " \
                                                           "and/or skos:narrowerTransitive."
        return message

    def find_concepts(self, graph):

        bad_concepts_list = []

        for concept in graph.subjects(RDF.type, SKOS.Concept):
            if any(((concept, SKOS.broaderTransitive, None) in graph,
                    (concept, SKOS.narrowerTransitive, None) in graph)):
                bad_concepts_list.append(concept)

        return bad_concepts_list
