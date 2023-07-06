import collections

from rdflib import RDF, SKOS, RDFS, URIRef

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class ValuelessAssociativeRelationsChecker(StructureTestInterfaceNavigate):
    """
    Checks if there are concepts in the graph that are related by the property skos:related and have the same narrower
    and broader concepts. These relations could overload the thesaurus with valueless relationships.
    check ISO/DIS 25964-1 for more info.
    """
    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with valueless associative relations."
        return message

    def find_concepts(self, graph):
        bad_concepts_list = set()
        related_concepts = []

        # Get every concept(-pair) that is related with skos:related predicate
        for concept, p, o in graph.triples((None, SKOS.related, None)):
            related_concepts.append((concept, o))
        # For each concept-tuple, get broader and narrower concepts and compare
        for pair in related_concepts:
            concept1, concept2 = pair
            broader_concepts1 = []
            broader_concepts2 = []

            for broader_concept in graph.objects(subject=concept1, predicate=SKOS.broader):
                broader_concepts1.append(broader_concept)
            for broader_concept in graph.objects(subject=concept2, predicate=SKOS.broader):
                broader_concepts2.append(broader_concept)
            # Check narrower relations from broader concepts
            for broader_concept in graph.subjects(predicate=SKOS.narrower, object=concept1):
                broader_concepts1.append(broader_concept)
            for broader_concept in graph.subjects(predicate=SKOS.narrower, object=concept2):
                broader_concepts2.append(broader_concept)

            same_broader_concepts = collections.Counter(broader_concepts1) == collections.Counter(broader_concepts2)

            if same_broader_concepts:  # and same_narrower_concepts
                bad_concepts_list.add(concept1)
                bad_concepts_list.add(concept2)
        return bad_concepts_list

