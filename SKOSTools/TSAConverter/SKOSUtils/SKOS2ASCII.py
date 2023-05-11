from TextExporter import TextWriter


class SKOS2ASCII:
    @staticmethod
    def write(skos_graph, pref_lang, filename=None):
        app = TextWriter(skos_graph, pref_lang)
        schemes = skos_graph.concept_schemes()
        for scheme in schemes:
            print(app.g.str_abbr(scheme))
            ascii = app.traverse(skos_graph.top_concepts(scheme))
            if filename:
                app.write_to_file(filename, ascii)
            else:
                print(ascii)



