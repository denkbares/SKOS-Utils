import logging

from rdflib import SKOS, RDF, Namespace, URIRef

from SKOSTools.SKOSQualityChecker.CheckerModules.StructureTestInterfaceNavigate import StructureTestInterfaceNavigate


class SinglePrefLabelChecker(StructureTestInterfaceNavigate):
    """
    Check whether every concept has at most one prefLabel for each language.
    Considers prefLabels defined in standard SKOS and SKOS-XL.
    """
    @property
    def status(self):
        return "Error"

    def message(self, result):
        if len(result) > 0:
            return "There are " + str(len(result)) + " concepts with multiple prefLabels for a single language."
        return ""

    def find_concepts(self, graph):
        bad_concepts_list = []
        for concept, p, o in graph.triples((None, RDF.type, SKOS.Concept)):
            # we need to separate vanilla and xl SKOS labels, since some ontologies define labels in both ways
            labels = self.all_pref_labels(concept, graph)
            the_lang = self.duplicate_labels(labels)
            if the_lang:
                self.send_log('<' + str(concept) + '> (' + the_lang + ')')
                bad_concepts_list.append(concept)
            labels_xl = self.all_pref_labels_xl(concept, graph)
            the_lang = self.duplicate_labels(labels_xl)
            if the_lang:
                self.send_log('<' + str(concept) + '> (' + the_lang + ')')
                bad_concepts_list.append(concept)

        self.send_log(str(len(bad_concepts_list)) + ' concepts with multiple prefLabels found.')
        return bad_concepts_list

    @staticmethod
    def duplicate_labels(labels):
        labels = list(labels)
        labels.sort(key=lambda l: l.language if l.language else "")
        for i in range(len(labels)):
            if (i+1) < len(labels):
                l1 = labels[i]
                l2 = labels[i+1]
                if l1.language == l2.language:
                    return str(l1.language)
        return False

