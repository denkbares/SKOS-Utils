from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class TopConceptIdentifier(StructureTestInterfaceNavigate):
    """
    Identify top concepts. "Keep the number of top concepts in any single concept scheme small (i.e., fewer than a half
    dozen)"
    We return all schemes that have more than 12 top concepts.
    Implements a part of the definition as described in:
    D. Allemang, J. A. Hendler, & F. Gandon, Semantic web for the working ontologist (2020). ACM Press.
    """

    def __init__(self):
        super().__init__()
        self.max_top_concepts = 12

    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 1:
            message = "There are " + str(len(result_df)) + \
                      " schemes with more than " + str(self.max_top_concepts) + \
                      " top concepts."
        elif len(result_df) == 1:
            message = "There is " + str(len(result_df)) + \
                      " scheme with more than " + str(self.max_top_concepts) + \
                      " top concepts."
        return message

    def find_concepts(self, graph):
        bad_concepts = set()
        for scheme, p, o in graph.triples((None, RDF.type, SKOS.ConceptScheme)):
            top_concepts = set()

            top_concepts.update(set(graph.triples((None, SKOS.topConceptOf, scheme))))
            top_concepts.update(set(graph.triples((scheme, SKOS.hasTopConcept, scheme))))
            if len(top_concepts) > self.max_top_concepts:
                bad_concepts.add(scheme)

        return bad_concepts

