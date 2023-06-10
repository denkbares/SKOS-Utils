from collections import defaultdict

import pandas as pd
import spacy
from rdflib import Graph
import rdflib.namespace


class POSAnalysis:
    """
    Analysis of the prefLabels for a given SKOS knowledge graph.
    For instance, you can count the usages of verb or nouns contained in the preLabels.
    """
    def __init__(self):
        # initialize the standard spacy models for some default languages
        self.spacy_model = {'FR': 'fr_core_news_sm', 'DE': 'en_core_web_sm', 'DE': 'de_core_news_sm'}

    def analyse(self, graph, language='EN', pos_tag='VERB'):
        """
        For a given graph all skos:prefLabels are extracted for a given language and the frequency
        of tokens is counted. The tokens need to have the defined pos_tag.
        :param graph: the given knowledge graph
        :param language: the language of interest of the skos:prefLabels
        :param pos_tag: the POS tag of the tokens to be counted
        :return: a DataFrame instance with the tokens and their frequencies
        """
        language = language.upper()
        count = defaultdict(int)
        if language in self.spacy_model:
            modelname = self.spacy_model[language]
        else:
            modelname = self.spacy_model["EN"]

        if modelname:
            nlp = spacy.load(modelname)

            for label in self.pref_labels(graph, language):
                doc = nlp(label)
                for token in doc:
                    if token.pos_ == pos_tag:
                        count[token.text] += 1

            token_col = []
            count_col = []
            for (t, c) in count.items():
                token_col.append(t)
                count_col.append(c)
            df = pd.DataFrame({'Token': token_col, 'Count': count_col})
            df = df.sort_values(by=['Count', "Token"], ascending=False)
            return df

    @staticmethod
    def pref_labels(graph, lang):
        labels = []
        qres = graph.query(
            "SELECT ?concept ?label WHERE { ?concept a skos:Concept ; skos:prefLabel ?label. " +
            "   FILTER(langMatches(lang(?label), \"" + lang + "\")) }",
            initNs={'skos': rdflib.namespace.SKOS}
        )
        for row in qres:
            labels.append(str(row[1]))
        return labels


if __name__ == "__main__":
    workspace_dir = '/Users/joba/denkCloud/Staff/Projekte/CLAAS/2019 TSA/Funktionen/Funktionen2023/_temp/'
    app = POSAnalysis()

    g = Graph()
    g.parse(workspace_dir+'Functions_CFUS_beta1_with_IDs.rdf', format='turtle')

    dataframe = app.analyse(g, language='de', pos_tag='VERB')
    dataframe.to_excel(workspace_dir+'verb_count.xlsx', index=False)

