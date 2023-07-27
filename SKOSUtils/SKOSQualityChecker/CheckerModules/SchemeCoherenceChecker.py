from rdflib import RDF, SKOS, RDFS, Literal

from SKOSUtils.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SchemeCoherenceChecker(StructureTestInterfaceNavigate):
    """
    Lists all SKOS concepts, for which the narrower and broader concepts
    are not in the same conceptScheme.
    Implements a part of the definition as described in:
    D. Allemang, J. A. Hendler, & F. Gandon, Semantic web for the working ontologist (2020). ACM Press.
    """
    @property
    def status(self):
        return "Warning"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " schemes with violated scheme coherence."
        return message

    def find_concepts(self, graph):
        bad_concepts = set()
        for concept, p, o in graph.triples((None, RDF.type, SKOS.Concept)):
            my_schemes = set(graph.objects(concept, SKOS.inScheme, None))
            # check whether all defined schemes of narrower concepts equal to the own scheme
            narrower_concepts = set(graph.objects(concept, SKOS.narrower, None))
            for narrower_concept in narrower_concepts:
                narrow_schemes = set(graph.objects(narrower_concept, SKOS.inScheme, None))
                if narrow_schemes:
                    if my_schemes != narrow_schemes:
                        bad_concepts.add(concept)
            # check whether all defined schemes of broader concepts equal to the own scheme
            broader_concepts = set(graph.objects(concept, SKOS.broader, None))
            for broader_concept in broader_concepts:
                broad_schemes = set(graph.objects(broader_concept, SKOS.inScheme, None))
                if broad_schemes:
                    if my_schemes != broad_schemes:
                        bad_concepts.add(concept)
        return bad_concepts


