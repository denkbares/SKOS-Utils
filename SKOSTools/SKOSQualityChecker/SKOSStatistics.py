import pandas as pd
import yaml
from rdflib import Graph, RDF, SKOS, Namespace, URIRef
from yaml import SafeLoader


class SKOSStatistics:
    def __init__(self, config_data):
        self.config_data = config_data

        self.NO_SCHEMES = 'Schemes'
        self.NO_CONCEPTS = 'Concepts'
        self.NO_PREF_LABELS = 'prefLabels'
        self.NO_XL_LABELS = 'prefLabels XL'
        self.NO_RELATION = 'Relations'
        self.NO_LANGUAGES = '#Languages'
        self.LANGUAGES = 'Languages'

        self.SKOSXL_NS = Namespace('http://www.w3.org/2008/05/skos-xl#')
        self.PREF_LABEL_XL = URIRef(self.SKOSXL_NS + 'prefLabel')
        self.LITERAL_FORM_XL = URIRef(self.SKOSXL_NS + 'literalForm')

    def compute_statistics(self):
        """Only direct relations/axioms are counted. No reasoning is provided."""
        df = pd.DataFrame({'name': [], self.NO_SCHEMES: [], self.NO_CONCEPTS: [],
                           self.NO_PREF_LABELS: [], self.NO_XL_LABELS: [], self.NO_RELATION: [],
                           self.NO_LANGUAGES: [], self.LANGUAGES: []})
        for graph in self.config_data['graphs']:
            for name, filename in graph.items():
                df = self.analyse(name, filename, df)
        return df

    def analyse(self, name, filename, df):
        graph = Graph()
        graph.parse(filename)
        schemes_count = sum(1 for _ in graph.triples((None, RDF.type, SKOS.ConceptScheme)))
        concept_count = sum(1 for _ in graph.triples((None, RDF.type, SKOS.Concept)))
        pref_label_count = sum(1 for _ in graph.triples((None, SKOS.prefLabel, None)))
        xl_labels_count = sum(1 for _ in graph.triples((None, self.LITERAL_FORM_XL, None)))
        relations_count = sum(1 for _ in graph.triples((None, None, None)))
        used_languages = self.identify_used_languages(graph)
        new_row = pd.Series([name, schemes_count, concept_count, pref_label_count,
                             xl_labels_count, relations_count, len(used_languages), str(used_languages)], index=df.columns)
        df = df._append(new_row, ignore_index=True)
        return df

    @staticmethod
    def write(df, output_file, sheet_name='SKOS Statistics'):
        with pd.ExcelWriter(output_file) as writer:
            df.to_excel(writer, sheet_name=sheet_name)

    def identify_used_languages(self, graph):
        used_languages = []
        for s, p, o in graph.triples((None, SKOS.prefLabel, None)):
            lang = o.language
            if lang not in used_languages:
                used_languages.append(lang)
        for s, p, o in graph.triples((None, self.LITERAL_FORM_XL, None)):
            lang = o.language
            if lang not in used_languages:
                used_languages.append(lang)
        return used_languages



if __name__ == '__main__':
    with open('configs/Statistics_config.yaml') as f:
        stats_config = yaml.load(f, Loader=SafeLoader)
    app = SKOSStatistics(stats_config)
    stats = app.compute_statistics()
    app.write(stats, stats_config['output'])
    print('Idle.')

