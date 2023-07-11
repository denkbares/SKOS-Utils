from rdflib import RDF, SKOS, RDFS

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class TopConceptIdentifier(StructureTestInterfaceNavigate):
    """
    Identify top concepts. "Keep the number of top concepts in any single concept scheme small (i.e., fewer than a half
    dozen)"
    Implements a part of the definition as described in:
    D. Allemang, J. A. Hendler, & F. Gandon, Semantic web for the working ontologist (2020). ACM Press.
    """
    @property
    def status(self):
        return "Info"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " top concepts in the given graph."
        return message

    def find_concepts(self, graph):
        top_concept_list = set()
        concepts_without_broader = set()
        narrower_concepts = set()

        for concept in graph.subjects(predicate=SKOS.topConceptOf):
            top_concept_list.add(concept)
        for o in graph.objects(predicate=SKOS.hasTopConcept):
            top_concept_list.add(o)
        # Concepts without broader and which are not narrower of other concepts
        for concept in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
            if (concept, SKOS.broader, None) not in graph:
                concepts_without_broader.add(concept)
            if (None, SKOS.narrower, concept) in graph:
                narrower_concepts.add(concept)

        final_concepts = concepts_without_broader - narrower_concepts

        for c in final_concepts:
            top_concept_list.add(c)

        return top_concept_list

