from rdflib import SKOS

from SKOSUtils.Converter.SKOSConverter import SKOSConverter

lns = 'http://www.example.org/skosutils#'
ns = {'ex': lns}

in_dir = 'tests/Testdata/'
out_dir = 'tests/Testdata/temp/'

rdf_file = 'Bike_Testdata.ttl'
xls_file = 'Bike_Testdata.xlsx'
xmind_file = 'Bike_Testdata.xmind'
dot_file = 'Bike_Testdata.dot'

# Hey ya, just choose a conversion from the list of commands
commands = ['rdf->xls', 'rdf->xmind', 'rdf->graphviz']
command = commands[2]

con = SKOSConverter(namespaces=ns, local_namespace=lns,
                    scheme_name="Example", preferred_language='en')
if command == 'rdf->xls':
    con.rdf_to_excel(rdf_file=in_dir+rdf_file, xls_file=out_dir+xls_file)
elif command == 'rdf->xmind':
    con.rdf_to_xmind(rdf_file=in_dir+rdf_file, xmind_file=out_dir+xmind_file)
elif command == 'rdf->graphviz':
    con.rdf_to_graphviz(rdf_file=in_dir+rdf_file, dot_file=out_dir+dot_file,
                        visited_relations=[SKOS.narrower],
                        html_nodes=True,
                        html_nodes_with_rdftype=True,
                        html_nodes_with_pref_labels=False,
                        dot_prolog=' rankdir=LR\n' +
                                   '  shape=plaintext\n' +
                                   ' node [fontname="Helvetica"]\n')
else:
    print('Please choose from one of the commands: ' + str(commands))
