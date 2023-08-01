import pandas as pd
from pandas import DataFrame
from rdflib import SKOS, Literal, Namespace

from SKOSUtils.Converter.ProcessUtils import ProcessUtils


class SKOS2XLS:
    def __init__(self, graph, prefered_language='en',
                 handled_properties=[SKOS.prefLabel, SKOS.altLabel, SKOS.note]):
        self.pref_lang = prefered_language
        self.graph = graph
        self.headers = []
        self.handled_properties = handled_properties
        self.headers_additions = []
        self.label_languages = []
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

        self.compute_headers(scheme)
        self.headers = ['Level', 'URI'] + self.headers_additions
        for hprop in self.handled_properties:
            for lang in self.label_languages:
                lang_add = ''
                if lang:
                    lang_add = '@' + lang
                self.headers.append(str(hprop) + lang_add)

        # iterate through graph by depth first search
        for concept in self.graph.top_concepts(scheme):
            self.traverse_rec(frame, level, concept)

        df = DataFrame(frame)
        df.columns = self.headers
        self.trim_columns(df)
        return df

    def compute_headers(self, scheme):
        for concept in self.graph.top_concepts(scheme):
            self.visit(concept)

    def visit(self, concept):
        used_notes = self.graph.note(concept)
        for ref in used_notes:
            note = str(ref.value)
            if note.startswith('@'):
                (attr, val) = ProcessUtils.separate_attr_val(note)
                if attr not in self.headers_additions and attr not in self.note_prefixes:
                    self.headers_additions.append(attr)
        for prop in self.handled_properties:
            lits = self.graph.g.objects(concept, prop)
            for literal in lits:
                if isinstance(literal, Literal):
                    lang = literal.language
                    if lang not in self.label_languages:
                        self.label_languages.append(lang)
        sorted_kids = self.sort(self.graph.narrower(concept))
        for kid in sorted_kids:
            self.visit(kid)

    def create_row(self, level, concept):
        # remove order and level notes, caution: we need 'order' for sorting before
        self.graph.trim_notes(concept, remove_with_prefixes=self.note_prefixes)

        row = dict.fromkeys(self.headers, [])

        row['Level'] = level
        row['URI'] = str(concept)
        for p in self.handled_properties:
            for lang in self.label_languages:
                value = self.value_for(concept, p, lang)
                lang_ext = ''
                if lang:
                    lang_ext = '@' + lang
                abbreviated_property = str(p)
                row[abbreviated_property + lang_ext] = value

        used_notes = self.graph.note(concept)
        for ref in used_notes:
            note = str(ref.value)
            if note.startswith('@'):
                (attr, val) = ProcessUtils.separate_attr_val(note)
                if attr in self.headers_additions:
                    row[attr] = val

        return row

    def traverse_rec(self, frame, level, concept):
        sorted_kids = self.sort(self.graph.narrower(concept))
        row = self.create_row(level, concept)
        frame.append(row)
        for kid in sorted_kids:
            self.traverse_rec(frame, level+1, kid)

    def sort(self, uri_list):
        # sort list by their order note
        uri_list = sorted(uri_list, key=lambda x: self.graph.order(x), reverse=False)
        return uri_list

    def value_for(self, concept, p, language=None):
        properties = self.graph.g.objects(concept, p)
        value = ''
        for ref in properties:
            if isinstance(ref, Literal) and ref.language == language:
                value = value + str(ref.value)
                value = value + '\n'
        if value.endswith('\n'):
            value = value[:len(value) - 1]
        return value

    @staticmethod
    def trim_columns(df):
        for col in df.columns:
            if col.startswith(Namespace(SKOS)):
                ncol = col.replace(Namespace(SKOS), 'skos:')
                df.rename(columns={col: ncol}, inplace=True)

