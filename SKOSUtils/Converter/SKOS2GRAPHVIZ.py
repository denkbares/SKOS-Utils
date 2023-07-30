from rdflib import SKOS, Literal


class SKOS2GRAPHVIZ:
    """
    This converter takes a graph (SKOS vocabulary) and generates a DOT file
    with all SKOS concepts as nodes connected by skos:narrower relations.
    You can pass a specific label function, that defines what should be printed as
    the primary label of each node.
    """
    def __init__(self, graph, preferred_language='en', prolog_definitions='', label_function=None,
                 html_nodes=False, html_nodes_with_pref_labels=True, html_nodes_with_rdftype=True,
                 visited_relations=[SKOS.narrower, SKOS.broader]):
        self.preferred_language = preferred_language
        self.graph = graph
        self.uri_node_map = {}
        self.buffer = ''
        self.counter = 0
        self.prolog_definitions = prolog_definitions
        self.label_function = label_function
        self.visited_relations=visited_relations
        self.html_nodes = html_nodes  # when false, then just simple rounded nodes with prefLabels in it
        self.html_nodes_with_rdftype = html_nodes_with_rdftype
        self.html_nodes_with_prefLabels = html_nodes_with_pref_labels

    def write(self, graph, filename):
        self.reset_buffer()
        self.uri_node_map = {}
        for concept in graph.all_concepts():
            self.create_node(concept)
        for scheme in graph.concept_schemes():
            self.create_node(scheme)
            for top_concept in graph.top_concepts(scheme):
                self.create_node(top_concept)
                self.create_link(scheme, top_concept, label_uri=SKOS.hasTopConcept)
        for link_uri in self.visited_relations:
            for c1, p, c2 in graph.g.triples((None, link_uri, None)):
                self.create_link(c1, c2, label_uri=link_uri)

        self.write_buffer(filename)

    def create_node(self, concept):
        if concept in self.uri_node_map:
            return  # the node has been already created
        node_id = self.node_id()
        node_str = '// ' + str(concept) + '\n'
        if self.html_nodes:
            node_str += self.create_html_node(concept, node_id)
        else:
            label = self.quote(self.label(concept, self.graph, self.preferred_language))
            node_str += node_id + ' [label="' + label + '"]\n'
        self.uri_node_map[concept] = node_id
        self.send_buffer(node_str)

    def create_literal_node(self, literal):
        node_id = self.node_id()
        litstr = str(literal)
        litstr = litstr.replace('\n', '<BR/>')
        node_str = node_id + ' [label="' + self.quote(litstr) + '"]'
        self.uri_node_map[literal] = node_id
        self.send_buffer(node_str)

    def create_html_node(self, concept, node_id):
        table_attributes = ' BORDER="0" CELLBORDER="1" CELLSPACING="0"'
        LEFT_ALIGN = ' ALIGN="LEFT"'
        HEADLINE = LEFT_ALIGN + ' BGCOLOR="gray"'
        SECTION = LEFT_ALIGN + ' BGCOLOR="ghostwhite"'
        res = node_id + ' [shape=plaintext label=<<TABLE ' + table_attributes + '>\n'

        if isinstance(concept, Literal):
            res += str(concept)
            if concept.language:
                res += self.create_table_row(' + concept.language + ')
        else:
            # The headline of the node
            concept_label = self.quote(self.label(concept, self.graph, self.preferred_language))
            res += self.create_table_row(concept_label + ' (' + self.preferred_language + ')',
                                         td_attributes=HEADLINE)
            # Type of the concept
            if self.html_nodes_with_rdftype:
                concept_type = self.graph.uri_type(concept)
                res += self.create_table_row(self.graph.qstr(concept_type), td_attributes=LEFT_ALIGN)

            # The other prefLabels
            if self.html_nodes_with_prefLabels:
                res += self.create_table_row('skos:prefLabel:', td_attributes=SECTION)
                for literal in self.graph.pref_label(concept, None):
                    lang = '-'
                    if literal.language:
                        lang = literal.language
                    if literal.language == self.preferred_language:
                        continue
                    res += self.create_table_row(str(literal) + ' (' + lang + ')', td_attributes=LEFT_ALIGN)
        return res + '</TABLE>>];\n'

    @staticmethod
    def create_table_row(row_str, td_attributes=''):
        indent = '   '
        return indent + '<TR><TD ' + td_attributes + '>' + row_str + '</TD></TR>\n'

    def create_link(self, uri_a, uri_b, label_uri=None):
        # in case that there is a Literal not created yet
        if uri_a not in self.uri_node_map:
            self.create_literal_node(uri_a)
        if uri_b not in self.uri_node_map:
            self.create_literal_node(uri_b)

        link_label = ' -> '
        link_str = self.uri_node_map[uri_a] + link_label + self.uri_node_map[uri_b]
        if label_uri:
            label_str = self.graph.qstr(label_uri)
            link_str += ' [label="' + label_str + '"]'

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
