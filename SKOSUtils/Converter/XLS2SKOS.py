import pandas as pd
from SKOSUtils.Converter.Generic2SKOS import Generic2SKOS
from SKOSUtils.Converter.SKOSConcept import SKOSConcept
from SKOSUtils.Converter.SKOSScheme import SKOSScheme


class XLS2SKOS(Generic2SKOS):
    def __init__(self, namespace, scheme_name, bindings={}, default_language='de'):
        self.last_entry_with_level = {}
        super().__init__(namespace, scheme_name, bindings=bindings, default_language=default_language)

    def read_dataframe(self, dataframe, level_col_name, value_col_name, uri_col_name=None,
                       note_col_name=None, hidden_label_col_name=None):
        self.scheme = SKOSScheme(self.scheme_name)

        for index, row in dataframe.iterrows():
            level = row[level_col_name]
            value = row[value_col_name]
            if note_col_name:
                notes = row[note_col_name]
            else:
                notes = ''
            if uri_col_name:
                uri = row[uri_col_name]
                # we check if there is an abbreviated namespace already defined, then cut it
                if ':' in uri:
                    namespace_index = uri.find(':')
                    if namespace_index:
                        uri = uri[namespace_index+1:]
            else:
                uri = None  # when None, then the URI is generated

            concept = SKOSConcept(value, uuid=uri, namespace=self.namespace)
            if hidden_label_col_name:
                concept.hiddenLabel = row[hidden_label_col_name]
            concept.order = index
            if notes != 'nan':
                concept.add_note(notes)
            if level == 1:
                self.scheme.add_top_concept(concept)
            else:
                broader_concept = self.last_entry_with_level[level - 1]
                concept.add_broader(broader_concept)
                broader_concept.add_narrower(concept)
            self.last_entry_with_level[level] = concept
        return self.scheme

    def read_xls(self, filename, level_col_name, value_col_name, note_col_name=None, uri_col_name=None, sheet_number=0):
        self.set_source_filename(filename)

        df = pd.read_excel(filename, sheet_name=sheet_number)
        df = df.drop(df[(df[level_col_name].isna())].index)
        df = df.drop(df[(df[value_col_name].isna())].index)
        if note_col_name:
            df = df.astype({level_col_name: 'int', value_col_name: 'str', note_col_name: 'str'})
        else:
            df = df.astype({level_col_name: 'int', value_col_name: 'str'})
        return self.read_dataframe(df, level_col_name=level_col_name, value_col_name=value_col_name,
                                   uri_col_name=uri_col_name, note_col_name=note_col_name, hidden_label_col_name='ID')
