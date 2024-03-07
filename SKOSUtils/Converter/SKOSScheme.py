from datetime import datetime


class SKOSScheme:
    def __init__(self, schemename='Noname'):
        self.name = schemename
        self.top_concepts = []
        self.scheme_uri = None
        current_datetime = datetime.now()
        self.generation_time = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def add_top_concept(self, concept):
        self.top_concepts.append(concept)

    def top_concepts(self):
        return self.top_concepts

    def to_str_rec(self, indent, concept):
        buffy = '-' * indent
        buffy += ' ' + concept.name
        if concept.notes:
            buffy += ' (' + ', '.join(concept.notes) + ')'
        buffy += ' [' + concept.uri + ']'
        buffy += '\n'
        kidindent = indent + 1
        for kid in concept.narrower:
            buffy += self.to_str_rec(kidindent, kid)
        return buffy

    def __str__(self):
        sss = ''
        for tc in self.top_concepts:
            sss += self.to_str_rec(0, tc)
        return sss

