from rdflib import RDF, SKOS, RDFS
from langcodes import Language
from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class InvalidLanguageTagChecker(StructureTestInterfaceNavigate):
    """
    Checks language tags against a list of all valid language tags defined in RFC3066.
    Implements a part of the definition as described in:
    O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
    Journal on Data Semantics 3 (2014). doi:10.1007/s13740-013-0026-0.
    """
    @property
    def status(self):
        return "Error"

    def message(self, result_df):
        message = ""
        if len(result_df) > 0:
            message = "There are " + str(len(result_df)) + " concepts with invalid language tags."
        return message

    def find_concepts(self, graph):
        bad_concepts_list = set()

        # Check language tags against a list of all language tags defined in RFC3066.
        for concept in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
            concept_labels = [self.all_pref_labels(concept, graph), self.all_pref_labels_xl(concept, graph)]
            concept_langs = self.get_all_used_languages(concept_labels)
            for lang in concept_langs:
                if not Language.get(lang).is_valid():
                    bad_concepts_list.add(concept)

        return bad_concepts_list

    @staticmethod
    def get_all_used_languages(labels):
        languages = []
        for label_list in labels:
            for label in label_list:
                if label.language is not None and not languages.__contains__(label.language):
                    languages.append(label.language)
        return languages
