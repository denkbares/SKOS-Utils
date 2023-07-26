import pandas as pd

from SKOSTools.Converter.Generic2SKOS import Generic2SKOS
from SKOSTools.Converter.SKOSConcept import SKOSConcept
from SKOSTools.Converter.SKOSScheme import SKOSScheme


class XLS2SKOS(Generic2SKOS):
    def __init__(self, namespace, scheme_name, bindings={}, default_language='de'):
        self.last_entry_with_level = {}
        super().__init__(namespace, scheme_name, bindings=bindings, default_language=default_language)

    def read_dataframe(self, dataframe, level_col, value_col, note_col=None):
        self.scheme = SKOSScheme(self.scheme_name)

        for index, row in dataframe.iterrows():
            level = row[level_col]
            value = row[value_col]
            if note_col:
                notes = row[note_col]
            else:
                notes = ''
            # todo check whether there is an ID in the Excel an reuse it!
            concept = SKOSConcept(value, namespace=self.namespace)
            concept.add_note('order', str(index))
            self.collect_and_add_notes(notes, concept)
            if level == 1:
                self.scheme.add_top_concept(concept)
            else:
                broader_concept = self.last_entry_with_level[level - 1]
                concept.add_broader(broader_concept)
                broader_concept.add_narrower(concept)
            self.last_entry_with_level[level] = concept
        return self.scheme

    def read_xls(self, filename, level_col, value_col, note_col=None, sheet_number=0):
        df = pd.read_excel(filename, sheet_name=sheet_number)
        df = df.drop(df[(df.Level.isna())].index)
        df = df.drop(df[(df.Name.isna())].index)
        if note_col:
            df = df.astype({level_col: 'int', value_col: 'str', note_col: 'str'})
        else:
            df = df.astype({level_col: 'int', value_col: 'str'})
        return self.read_dataframe(df, level_col, value_col, note_col)


