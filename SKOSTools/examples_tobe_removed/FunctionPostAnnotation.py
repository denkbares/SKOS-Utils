import os
import sys
from SKOSTools import UtilDir
from SKOSTools.UtilDir.SKOSGraph import SKOSGraph
from SKOSTools.Converter.SKOSConverter import SKOSConverter
from SKOSTools.examples_tobe_removed.SKOS2SAPXLS import SKOS2SAPXLS
from SKOSTools.examples_tobe_removed.SegmentIDAdder import SegmentIDAdder

UtilDir.activate_venv()
sys.path.append(os.path.join(os.path.abspath(".."), "SKOSUtils"))

workspace = '/Users/joba/denkCloud/Staff/Projekte/CLAAS/2019 TSA/Funktionen/Funktionen2023/_temp/'
out_name_prefix = 'Functions_CFUS_beta1'

xmind_in_filename = workspace + 'Original_Functions_v44.xmind'
xmind_out_filename = workspace + out_name_prefix + '.xmind'
rdf_filename = workspace + out_name_prefix + '.rdf'
rdf_filename_modified = workspace + out_name_prefix + '_with_IDs.rdf'
xls_filename = workspace + out_name_prefix + '.xlsx'

ns = {'cfus': 'http://www.claas.com/cfus#'}
lns = 'http://www.claas.com/cfus#'

con = SKOSConverter(namespaces=ns, local_namespace=lns, scheme_name="Functions", preferred_language='de')

# We first convert the original XMind file to RDF
con.xmind_to_rdf(xmind_in_filename, rdf_filename)

# The RDF is annotated with Segmented IDs
id_augmenter = SegmentIDAdder()
id_augmenter.augment(rdf_filename, rdf_filename_modified, namespaces=ns)

# The annotated RDF is converted back to a XMind
con.rdf_to_xmind(rdf_filename_modified, xmind_out_filename)

# The annotated RDF is converted to Excel (we use a modified version of the XLS output)
con.rdf_to_excel(xls_filename, rdf_filename_modified)
graph = SKOSGraph(rdf_filename_modified, ns)
skos2sapxls = SKOS2SAPXLS(graph)
skos2sapxls.write(xls_filename=xls_filename)



