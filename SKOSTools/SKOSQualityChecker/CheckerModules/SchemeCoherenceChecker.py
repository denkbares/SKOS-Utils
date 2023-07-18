from rdflib import RDF, SKOS, RDFS, Literal

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SchemeCoherenceChecker(StructureTestInterfaceNavigate):
    """
    Check if narrower and broader concepts of a concept are in the same conceptScheme.
    Implements a part of the definition as described in:
    D. Allemang, J. A. Hendler, & F. Gandon, Semantic web for the working ontologist (2020). ACM Press.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with violated scheme coherence."
        return message

    # def find_concepts(self, graph):
    #     bad_concepts = set()
    #     narrower_and_broader_concepts = set()
    #     for concept, p, scheme in graph.triples((None, SKOS.inScheme, None)):
    #         for narrower_concept in graph.objects(concept, SKOS.narrower, None):
    #             narrower_and_broader_concepts.add(narrower_concept)
    #         for broader_concept in graph.objects(concept, SKOS.broader, None):
    #             narrower_and_broader_concepts.add(broader_concept)
    #
    #         for other_concept in narrower_and_broader_concepts:
    #             other_scheme = graph.value(subject=other_concept, predicate=SKOS.inScheme)
    #             if Literal(scheme) != Literal(other_scheme):
    #                 bad_concepts.add(concept)
    #
    #     return bad_concepts

    def find_concepts(self, graph):
        bad_concepts = set()
        narrower_and_broader_concepts = {}

        for concept, p, scheme in graph.triples((None, SKOS.inScheme, None)):
            narrower_concepts = set(graph.objects(concept, SKOS.narrower, None))
            broader_concepts = set(graph.objects(concept, SKOS.broader, None))

            for narrower_concept in narrower_concepts:
                narrower_and_broader_concepts[narrower_concept] = scheme

            for broader_concept in broader_concepts:
                narrower_and_broader_concepts[broader_concept] = scheme

        for concept, scheme in narrower_and_broader_concepts.items():
            other_scheme = graph.value(subject=concept, predicate=SKOS.inScheme)
            if Literal(scheme) != Literal(other_scheme):
                bad_concepts.add(concept)

        return bad_concepts


