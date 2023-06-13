from rdflib import Graph


class QuickRDFConverter:
    """
    This small scripts is usable to convert ontologies from one format syntax into another, e.g., from XML to Turtle.
    """
    def convert(self, in_file, out_file, in_syntax=None, out_syntax='ttl'):
        g = Graph()
        if in_syntax:
            g.parse(in_file, format=in_syntax)
        else:
            g.parse(in_file)
        g.serialize(destination=out_file, format=out_syntax)


if __name__ == '__main__':
    in_file = '/Users/joba/Downloads/eurovoc-skos-ap-eu.rdf'
    out_file = '/Users/joba/Downloads/eurovoc-skos-ap-eu.ttl'
    app = QuickRDFConverter()
    app.convert(in_file=in_file, out_file=out_file, in_syntax='xml', out_syntax='ttl')