import os
import sys

from SKOSUtils import UtilDir
from SKOSUtils.Converter.SKOSConverter import SKOSConverter

UtilDir.activate_venv()
sys.path.append(os.path.join(os.path.abspath(".."), "SKOSUtils"))

workspace = '/Users/joba/Documents/_research/2023-SKOS-UtilDir/data/'
xmind_in_filename = workspace + 'Bike_Testdata_Paper.xmind'
rdf_outfile = workspace + 'Bike_Testdata_Paper.rdf'
xls_filename = workspace + 'Bike_Testdata_Paper.xlsx'

lns = 'http://www.example.org/skosutils#'
ns = {'ex': lns}
con = SKOSConverter(namespaces=ns, local_namespace=lns, scheme_name="Functions", preferred_language='de')

# We first convert the original XMind file to RDF
con.xmind_to_rdf(xmind_in_filename, rdf_outfile, sheet_no=0)

con.rdf_to_excel(xls_filename, rdf_outfile)
