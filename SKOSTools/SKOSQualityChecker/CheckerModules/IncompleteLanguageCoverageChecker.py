from rdflib import RDF, SKOS, RDFS
from langcodes import Language
from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class IncompleteLanguageCoverageChecker(StructureTestInterfaceNavigate):
    """
    Checks language tags against a list of all language used in the graph.
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
            message = "There are " + str(len(result_df)) + " concepts with incomplete language coverage."
        return message

    def find_concepts(self, graph):
        bad_concepts_list = []
        global_labels = []

        concepts = list(graph.subjects(predicate=RDF.type, object=SKOS.Concept))
        for concept in concepts:
            # we need to separate vanilla and xl SKOS labels, since some ontologies define labels in both ways
            global_labels.append(self.all_pref_labels(concept, graph))
            global_labels.append(self.all_pref_labels_xl(concept, graph))
        # Get all languages used in the graph
        global_langs = self.get_all_used_languages(global_labels)

        # Check global_langs against valid language tags
        for lang in global_langs.copy():
            if not Language.get(lang).is_valid():
                global_langs.remove(lang)

        for concept in concepts:
            concept_labels = [self.all_pref_labels(concept, graph), self.all_pref_labels_xl(concept, graph)]
            concept_langs = self.get_all_used_languages(concept_labels)
            if not all(element in concept_langs for element in global_langs):
                bad_concepts_list.append(concept)

        return bad_concepts_list

    @staticmethod
    def get_all_used_languages(labels):
        languages = set()
        for label_list in labels:
            for label in label_list:
                if label.language is not None:  # and not languages.__contains__(label.language):
                    languages.add(label.language)
        return languages
