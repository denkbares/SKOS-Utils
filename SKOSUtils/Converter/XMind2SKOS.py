from xmindparser import xmind_to_dict
import re

from SKOSUtils.Converter.Generic2SKOS import Generic2SKOS
from SKOSUtils.Converter.SKOSConcept import SKOSConcept
from SKOSUtils.Converter.SKOSScheme import SKOSScheme


class XMind2SKOS(Generic2SKOS):
    def __init__(self, namespace, scheme_name, bindings={}, default_language='de'):
        super(XMind2SKOS, self).__init__(namespace, scheme_name, bindings=bindings, default_language=default_language)
        self.counter = 0
        self.max_depth = None

    def handle_concept(self, concept):
        pass

    def traverse_rec(self, topic, current_depth, parent_topic=None, order=None):
        if self.max_depth:
            if self.max_depth == current_depth:
                return
        current_depth += 1
        self.counter += 1
        title = topic['title']
        children = topic['topics'] if 'topics' in topic else []

        notes = self.split_notes(topic['note']) if 'note' in topic else ''
        # adapt the order value according to the actual order in the topics-list
        uuid = None
        if notes and order:
            for i, note in enumerate(notes):
                if '@order:' in note:
                    notes[i] = re.sub('@order:\\s\\d+', '@order: ' + str(order), note)
                elif note.startswith('@uuid:'):
                    uuid = notes[i][6:].strip()

        concept = SKOSConcept(title, note=notes, namespace=self.namespace, uuid=uuid, uuid_prefix='Fu_')
        concept.add_note('order', str(self.counter))
        if parent_topic:
            concept.add_broader(parent_topic)
            parent_topic.add_narrower(concept)
        else:
            self.scheme.add_top_concept(concept)
        self.handle_concept(concept)
        kid_count = 0
        for kid in children:
            kid_count += 10
            self.traverse_rec(current_depth=current_depth, topic=kid, parent_topic=concept, order=kid_count)

    def split_notes(self, notes):
        return notes.split('\n')

    # start from root and create skos concepts
    def traverse(self, sheet, xmind_root_node_title=None, current_depth=0):
        self.counter = 0
        root_topic = sheet['topic']
        if xmind_root_node_title:
            # find the node with the given title and traverse from this one
            root_topic = self.find_node(root_topic, xmind_root_node_title)
        if root_topic:
            self.traverse_rec(root_topic, current_depth=current_depth)
        else:
            raise ValueError('The given root node does not exist in XMind sheet.')

    def read_xmind(self, xmind_file, rdf_file, sheet_no=0, xmind_root_node_title=None, max_depth=None):
        self.set_source_filename(xmind_file)
        self.scheme = SKOSScheme(self.scheme_name)
        self.max_depth = max_depth
        xmind_dict = xmind_to_dict(xmind_file)
        # take the first sheet in the XMind workbook
        self.traverse(xmind_dict[sheet_no], xmind_root_node_title=xmind_root_node_title)
        self.to_rdf(self.scheme, rdf_file)

    def find_node(self, topic, node_title):
        title = topic['title']
        if title == node_title:
            return topic
        else:
            kids = topic['topics'] if 'topics' in topic else []
            for kid in kids:
                node = self.find_node(kid, node_title)
                if node:
                    return node

