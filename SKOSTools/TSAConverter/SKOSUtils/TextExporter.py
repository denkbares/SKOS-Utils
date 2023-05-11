from SKOSTools.skosutils.SKOSTraversal import SKOSTraversal


class TextWriter(SKOSTraversal):
    def handle(self, indent, concept, parent_concept):
        s = ''
        s += '    ' * indent
        s += '|-- ' + self.print_label(concept)
        s += ' (' + self.abbr_id(concept) + ')'
        if self.g.plain_notes(concept):
            s += '\n' + '    ' * indent + '|   ' + self.g.plain_notes(concept)
        self.stack += s + '\n'
