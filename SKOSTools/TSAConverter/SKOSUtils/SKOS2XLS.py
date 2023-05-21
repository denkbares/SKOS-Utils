import pandas as pd
from pandas import DataFrame


class SKOS2XLS:
    def __init__(self, graph, prefered_language='en'):
        self.pref_lang = prefered_language
        self.graph = graph
        self.headers = ['Level', 'Name', 'Notes']
        self.note_prefixes = ['@order', 'order', '@level', 'level']

    def write(self, xls_filename):
        schemes = self.graph.concept_schemes()
        # Open the Excel file
        writer = pd.ExcelWriter(xls_filename, engine='xlsxwriter')
        # Make a sheet for each scheme
        for scheme in schemes:
            df = self.as_dataframe(scheme)
            df.to_excel(writer, sheet_name=self.graph.pref_label(scheme, lang=self.pref_lang), index=False)
        writer.close()

    def as_dataframe(self, scheme):
        frame = []
        level = 1
        # iterate through graph as depth first search
        for concept in self.graph.top_concepts(scheme):
            self.traverse_rec(frame, level, concept)
        df = DataFrame(frame)
        df.columns = self.headers
        return df

    def traverse_rec(self, frame, level, concept):
        sorted_kids = self.sort(self.graph.narrower(concept))
        # remove order and level notes, caution: we need 'order' for sorting before
        self.graph.trim_notes(concept, remove_with_prefixes=self.note_prefixes)
        if self.graph.plain_notes(concept):
            the_notes = self.graph.plain_notes(concept)
        else:
            the_notes = ''
        row = [level, self.graph.pref_label(concept, self.pref_lang), the_notes]
        frame.append(row)
        for kid in sorted_kids:
            self.traverse_rec(frame, level+1, kid)

    def sort(self, uri_list):
        # sort list by their order note
        uri_list = sorted(uri_list, key=lambda x: self.graph.order(x), reverse=False)
        return uri_list
