from SKOSTools.TSAConverter.SKOSUtils.SKOS2XLS import SKOS2XLS


class SKOS2XLSLegacy (SKOS2XLS):
    def __init__(self, graph, prefered_language='en'):
        self.pref_lang = prefered_language
        self.graph = graph
        self.headers = ['Level', 'Name', 'Notes']
        self.note_prefixes = ['@order', 'order', '@level', 'level']

    def create_row(self, level, concept):
        # remove order and level notes, caution: we need 'order' for sorting before
        self.graph.trim_notes(concept, remove_with_prefixes=self.note_prefixes)
        if self.graph.plain_notes(concept):
            the_notes = self.graph.plain_notes(concept)
        else:
            the_notes = ''
        return [level, self.graph.pref_label(concept, self.pref_lang), the_notes]
