from rdflib import RDF, SKOS, RDFS
from langcodes import Language
from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class IncompleteLanguageCoverageChecker(StructureTestInterfaceNavigate):
    """
    The set of all used language tags used in the vocabulary is computed.
    The check lists all SKOS concepts, that have labels only for
    a subset of languages defined.
    See O. Suominen, C. Mader, Assessing and improving the quality of skos vocabularies,
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
        global_labels = set()
        # We first retrieve all use languages in general from all SKOS concepts
        concepts = set(graph.subjects(predicate=RDF.type, object=SKOS.Concept))
        for concept in concepts:
            # we need to separate vanilla and xl SKOS labels, since some ontologies define labels in both ways
            global_labels.update(self.all_pref_labels(concept, graph))
            global_labels.update(self.all_pref_labels_xl(concept, graph))
        # Get all languages used in the graph
        global_langs = self.get_all_used_languages(global_labels)

        # Check global_langs against valid language tags
        for lang in global_langs.copy():
            if not Language.get(lang).is_valid():
                global_langs.remove(lang)

        # Now we check whether for all concepts all detected languages are used
        for concept in concepts:
            concept_labels = set(self.all_pref_labels(concept, graph))
            concept_labels.update(self.all_pref_labels_xl(concept, graph))
            concept_langs = self.get_all_used_languages(concept_labels)

            missing_langs = global_langs.difference(concept_langs)
            if missing_langs:
                bad_concepts_list.append(concept)
                missing_langs = global_langs.difference(concept_langs)
                self.send_log(str(concept) + ' has missing languages: ' + str(missing_langs))

        return bad_concepts_list

    @staticmethod
    def get_all_used_languages(labels):
        languages = set()
        for label in labels:
            lang = label.language
            if lang is not None:
                languages.add(label.language)
        return languages
