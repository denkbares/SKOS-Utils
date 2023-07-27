import xmind
import os.path

from SKOSUtils.Converter.XMindWriter import XMindWriter


class SKOS2XMind:
    @staticmethod
    def write(skos_graph, xmind_filename, preferred_language):
        xmindapp = XMindWriter(skos_graph, pref_lang=preferred_language)
        schemes = skos_graph.concept_schemes()

        # check whether file already exists, then delete it
        if os.path.isfile(xmind_filename):
            os.remove(xmind_filename)

        xmindapp.workbook = xmind.load(xmind_filename)
        for scheme in schemes:
            xmindapp.traverse(scheme)
        xmind.save(xmindapp.workbook, path=xmind_filename)
