from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class OrphanConceptChecker(StructureTestInterfaceNavigate):
    """
    Identify concepts without any relation to another concept.
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
            message = "There are " + str(len(result_df)) + " concepts without any associative or " \
                                                           "hierarchical relationships."
        return message

    def find_concepts(self, graph):
        bad_concept_list = []
        for concept in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
            if not any(((concept, SKOS.related, None) in graph,
                        (None, SKOS.related, concept) in graph,
                        (concept, SKOS.broader, None) in graph,
                        (None, SKOS.broader, concept) in graph,
                        (concept, SKOS.narrower, None) in graph,
                        (None, SKOS.narrower, concept) in graph,
                        (concept, SKOS.hasTopConcept, None) in graph,
                        (None, SKOS.hasTopConcept, concept) in graph,
                        (concept, SKOS.topConceptOf, None) in graph,
                        (None, SKOS.topConceptOf, concept) in graph)):
                bad_concept_list.append(concept)
        return bad_concept_list
