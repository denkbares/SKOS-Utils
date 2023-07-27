from SKOSUtils.Converter.SKOS2XLS import SKOS2XLS


class SKOS2SAPXLS(SKOS2XLS):
    def __init__(self, graph, prefered_language='de'):
        super().__init__(graph, prefered_language)
        self.headers = ['Level', 'UUID', 'Segment ID', 'Name', 'Phrase', 'Notes']

    def traverse_rec(self, frame, level, concept):
        sorted_kids = self.sort(self.graph.narrower(concept))
        # remove order and level notes, caution: we need 'order' for sorting before
        self.graph.trim_notes(concept, remove_with_prefixes=self.note_prefixes)
        uuid = self.get_from_note(concept, '@uuid:')
        segmented_id = self.get_from_note(concept, '@segment_id:')
        phrase = self.get_from_note(concept, '@phrase:', stip_quotation_marks=True)
        the_notes = self.all_remaining_notes_without(concept, ['@uuid:', '@segment_id:', '@phrase:'])

        row = [level, uuid, segmented_id, self.graph.pref_label(concept, self.pref_lang), phrase, the_notes]
        frame.append(row)
        for kid in sorted_kids:
            self.traverse_rec(frame, level+1, kid)

    def get_from_note(self, uri, prefix, stip_quotation_marks=False):
        uuid = self.graph.note_with_prefix(uri, prefix)
        if uuid:
            s = uuid[len(prefix):].strip()
            if stip_quotation_marks:
                if s.startswith('"'):
                    s = s[1:]
                if s.endswith('"'):
                    s = s[:-1]
            return s
        else:
            return ""

    def all_remaining_notes_without(self, uri, exclude_prefixes=[]):
        referred_objects = self.graph.note(uri)
        note = ''
        for ref in referred_objects:
            s = str(ref.value)
            include = True
            for exclude in exclude_prefixes:
                if s.startswith(exclude):
                    include = False
            if include:
                note = note + s
                note = note + '\n'
        return note[:len(note) - 1]
