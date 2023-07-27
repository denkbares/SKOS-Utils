from rdflib import Graph, Namespace


class QuickRDFConverter:
    """
    This small scripts is usable to convert ontologies from one format syntax into another, e.g., from XML to Turtle.
    """
    def convert(self, in_file, out_file, in_syntax=None, out_syntax='ttl'):
        g = Graph()
        g.bind('skos', Namespace('http://www.w3.org/2004/02/skos/core#'))
        g.bind('skosxl', Namespace('http://www.w3.org/2008/05/skos-xl#'))
        g.bind('dc', Namespace('http://purl.org/dc/terms/'))
        g.bind('agroont', Namespace('http://aims.fao.org/aos/agrontology#'))
        g.bind('agrovoc', Namespace('http://aims.fao.org/aos/agrovoc/'))
        g.bind('eurovoc', Namespace('http://eurovoc.europa.eu/'))
        g.bind('euroconstat', Namespace('http://publications.europa.eu/resource/authority/concept-status/'))
        g.bind('eurolabeltype', Namespace('http://publications.europa.eu/resource/authority/label-type/'))
        if in_syntax:
            g.parse(in_file, format=in_syntax)
        else:
            g.parse(in_file)
        g.serialize(destination=out_file, format=out_syntax)


if __name__ == '__main__':
    #in_file = '/Users/joba/denkbares/skos-tools/tests/Testdata/Bike_Testdata_Original.ttl'
    #out_file = '/Users/joba/denkbares/skos-tools/tests/Testdata/Bike_Testdata_Original.rdf'

    in_file = '/Users/joba/Downloads/datasets/geonames_ontology_v3.3.rdf'
    out_file = '/Users/joba/Downloads/datasets/geonames_ontology_v3.3.ttl'
    app = QuickRDFConverter()
    app.convert(in_file=in_file, out_file=out_file, in_syntax='ttl', out_syntax='xml')