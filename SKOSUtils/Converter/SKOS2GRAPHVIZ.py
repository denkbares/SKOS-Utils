from rdflib import SKOS


class SKOS2GRAPHVIZ:
    """
    This converter takes a graph (SKOS vocabulary) and generates a DOT file
    with all SKOS concepts as nodes connected by skos:narrower relations.
    You can pass a specific label function, that defines what should be printed as
    the primary label of each node.
    """
    def __init__(self, graph, preferred_language='en', prolog_definitions='', label_function=None):
        self.preferred_language = preferred_language
        self.graph = graph
        self.uri_node_map = {}
        self.buffer = ''
        self.counter = 0
        self.prolog_definitions = prolog_definitions
        self.label_function = label_function

    def write(self, graph, filename):
        self.reset_buffer()
        self.uri_node_map = {}
        for concept in graph.all_concepts():
            self.create_node(concept)
        for scheme in graph.concept_schemes():
            self.create_node(scheme)
            for top_concept in graph.top_concepts(scheme):
                self.create_node(top_concept)
                self.create_link(scheme, top_concept, label='top concept')
        for c1, p, c2 in graph.g.triples((None, SKOS.narrower, None)):
            self.create_link(c1, c2, label='narrower')
        self.write_buffer(filename)

    def dfs_visit_links(self, graph, parent, child):
        self.create_link(parent, child, label='narrower')
        for kid in graph.narrower(child):
            self.dfs_visit_links(graph, child, kid)

    def create_node(self, concept, plain=True):
        label = self.quote(self.label(concept, self.graph, self.preferred_language))
        node_id = self.node_id()
        node_str = '// ' + str(concept) + '\n'
        if plain:
            node_str += node_id + ' [label="' + label + '"]\n'
        else:
            node_str += node_id + ' [label=<<TABLE><TR><TD>' + label \
                       + '</TD></TR>\n<TR><TD>caption</TD></TR></TABLE>>];\n'
        self.uri_node_map[concept] = node_id
        self.send_buffer(node_str)

    def create_link(self, uri_a, uri_b, label=''):
        link_label = ' -> '
        link_str = self.uri_node_map[uri_a] + link_label + self.uri_node_map[uri_b]
        if label:
            link_str += ' [label="' + self.quote(label) + '"]'

        self.send_buffer(link_str)

    def label(self, concept, graph, preferred_language='en'):
        if self.label_function:
            return self.label_function(concept, graph, preferred_language)
        else:
            return graph.pref_label(concept, preferred_language)

    def node_id(self):
        self.counter += 1
        return 'node_' + str(self.counter)

    def send_buffer(self, node_str):
        self.buffer += node_str + '\n'

    def reset_buffer(self, graph_name='generated_graph'):
        self.buffer = 'digraph ' + graph_name + ' {\n' + self.prolog_definitions + '\n'

    def write_buffer(self, filename):
        self.buffer += '\n}\n'
        with open(filename, 'w') as f:
            f.write(self.buffer)

    @staticmethod
    def quote(s):
        return s.replace('"', "'")
