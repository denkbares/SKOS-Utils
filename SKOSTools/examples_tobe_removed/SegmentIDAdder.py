from rdflib import SKOS, Literal

from SKOSTools.UtilDir.SKOSGraph import SKOSGraph


class SegmentIDAdder:
    def __init__(self, prefered_language='de', number_of_digits_per_segment=3):
        self.graph = None
        self.note_prefixes = []
        self.pref_lang = prefered_language
        self.number_of_digits_per_segment = number_of_digits_per_segment

    def traverse_rec(self, level, concept, parent_segment_id='', my_segment_id=None):
        sorted_kids = self.sort(self.graph.narrower(concept))
        # remove order and level notes, caution: we need 'order' for sorting before
        self.graph.trim_notes(concept, remove_with_prefixes=self.note_prefixes)

        seg_id = ''
        if my_segment_id:
            my_segment_id_as_str = self.make_segmentid_as_string(my_segment_id)
            if parent_segment_id:
                seg_id = parent_segment_id + '.' + my_segment_id_as_str
            else:
                seg_id = 'F' + my_segment_id_as_str
            self.graph.g.add((concept, SKOS.note, Literal('@segment_id: ' + seg_id)))
            augmented_label = seg_id + ' ' + self.graph.pref_label(concept, self.pref_lang)
            self.graph.g.add((concept, SKOS.altLabel, Literal(augmented_label, self.pref_lang)))

        inc = self.compute_increase_shift(sorted_kids)
        my_inc = 0
        for kid in sorted_kids:
            my_inc = my_inc + inc
            self.traverse_rec(level + 1, kid, parent_segment_id=seg_id, my_segment_id=my_inc)

    def sort(self, uri_list):
        # sort list by their order note
        uri_list = sorted(uri_list, key=lambda x: self.graph.order(x), reverse=False)
        return uri_list

    def traverse(self):
        schemes = self.graph.concept_schemes()
        for scheme in schemes:
            level = 1
            for concept in self.graph.top_concepts(scheme):
                self.traverse_rec(level, concept)

    def save(self, filename):
        self.graph.g.serialize(format='turtle', destination=filename)

    def make_segmentid_as_string(self, raw_id):
        s_id = str(raw_id)
        missing_zeros = self.number_of_digits_per_segment - len(s_id)
        if missing_zeros > 0:
            s_id = s_id.zfill(self.number_of_digits_per_segment)
        return s_id

    def augment(self, in_rdffile, out_rdffile, namespaces={}):
        self.graph = SKOSGraph(in_rdffile, namespaces)
        self.traverse()
        self.save(out_rdffile)

    @staticmethod
    def compute_increase_shift(sorted_kids):
        count = len(sorted_kids)
        if count < 5:
            inc = 20
        elif count < 10:
            inc = 10
        elif count < 20:
            inc = 5
        else:
            inc = round(100 / count)
        return inc
