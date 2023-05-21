import abc

from rdflib import Literal


class SKOSTraversal:
    def __init__(self, graph, pref_lang='en'):
        self.g = graph
        self.stack = ''
        self.preferred_lang = pref_lang

    @abc.abstractmethod
    def handle(self, indent, concept, parent_concept):
        return

    def tos(self, generator):
        if isinstance(generator, list):
            return ' '.join(str(e) for e in generator)
        else:
            return str(generator)

    def print_label(self, uri):
        alt_label = self.g.alt_label(uri,self.preferred_lang)
        if isinstance(alt_label, Literal):
            return self.tos(alt_label)
        else:
            return self.tos(self.g.pref_label(uri, self.preferred_lang))

    def abbr_id(self, uri):
        return self.g.str_abbr(uri)

    def traverse(self, top_concepts):
        indent = 0
        self.stack = ''
        for tc in top_concepts:
            self.to_traverse_rec(indent, tc, None)
        return self.stack

    def to_traverse_rec(self, indent, concept, parent_concept):
        self.handle(indent, concept, parent_concept)
        indent += 1
        children = sorted(list(self.g.narrower(concept)))
        for child in children:
            self.to_traverse_rec(indent, child, concept)

    @staticmethod
    def write_to_file(filename, content):
        with open(filename, "w") as text_file:
            text_file.write(content)