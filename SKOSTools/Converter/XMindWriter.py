from xmind.core.topic import TopicElement

from SKOSTools.Converter.SKOSTraversal import SKOSTraversal


class XMindWriter(SKOSTraversal):
    def __init__(self, graph, pref_lang='en'):
        self.workbook = None
        self.topics = {}
        super(XMindWriter, self).__init__(graph, pref_lang)

    def handle(self, indent, concept, parent_concept):
        pass

    def traverse(self, scheme):
        sheet = self.workbook.createSheet()
        sheet.setTitle(self.abbr_id(scheme))
        for top_concept in sorted(self.g.top_concepts(scheme)):
            self.connect(sheet, scheme, top_concept)
            top_topic = self.get_topic(top_concept, sheet)
            sheet.getRootTopic().addSubTopic(top_topic)
            self.traverse_r(sheet, top_concept)

    def traverse_r(self, sheet, concept):
        narrowers = self.g.narrower(concept)
        for narrow in sorted(narrowers, key=lambda x: self.g.order(x), reverse=False):
            self.connect(sheet, concept, narrow)
            self.traverse_r(sheet, narrow)

    def connect(self, sheet, u1, u2):
        u1_topic = self.get_topic(u1, sheet)
        u2_topic = self.get_topic(u2, sheet)
        u1_topic.addSubTopic(u2_topic)
        u1_topic.setFolded()

    def get_topic(self, uri, sheet):
        if uri in self.topics:
            return self.topics[uri]
        else:
            topic = TopicElement(ownerWorkbook=sheet)
            label = self.print_label(uri)
            topic.setTitle(label)
            self.topics[uri] = topic
            plain_notes = self.g.plain_notes(uri)
            if plain_notes:
                topic.setPlainNotes(plain_notes)
            return topic

