import os

from SKOSUtils import UtilDir, Utils
from SKOSUtils.Converter.SKOS2ASCII import SKOS2ASCII
from SKOSUtils.Converter.SKOS2GRAPHVIZ import SKOS2GRAPHVIZ

from SKOSUtils.Converter.SKOS2XLS import SKOS2XLS
from SKOSUtils.Converter.SKOS2XMind import SKOS2XMind
from SKOSUtils.UtilDir.SKOSGraph import SKOSGraph
from SKOSUtils.Converter.XLS2SKOS import XLS2SKOS
from SKOSUtils.Converter.XMind2SKOS import XMind2SKOS

Utils.activate_venv()
from rdflib import Namespace, SKOS
import typer
import yaml
from yaml.loader import SafeLoader

converterApp = typer.Typer()


def create_converter():
    # Open the file and load the file
    with open('configs/TSAConverter_config.yaml') as f:
        config_data = yaml.load(f, Loader=SafeLoader)
    # define the namespace, in which the newly generated concepts are located
    local_namespace = Namespace(config_data["name_space"])
    namespaces = {config_data["name_space"]: config_data["name_space_key"]}
    scheme_name = config_data["scheme_name"]
    preferred_language = config_data["preferred_language"]

    result_converter = SKOSConverter(namespaces, local_namespace, scheme_name, preferred_language)

    if "input_directory" in config_data:
        result_converter.input_directory = config_data["input_directory"]
    else:
        root_path = Utils.get_project_root()
        result_converter.input_directory = os.path.join(root_path, "data")
    if "output_directory" in config_data:
        result_converter.output_directory = config_data["output_directory"]
    else:
        root_path = Utils.get_project_root()
        result_converter.output_directory = os.path.join(root_path, "data")
    if "file_name_prefix" in config_data:
        result_converter.file_name_prefix = config_data["file_name_prefix"]
    else:
        result_converter.file_name_prefix = "temp_file"
    if "xMind_root_title" in config_data:
        result_converter.xmind_root_node_title = config_data["xMind_root_title"]
    else:
        result_converter.xmind_root_node_title = None

    return result_converter


class SKOSConverter:
    def __init__(self, namespaces, local_namespace, scheme_name, preferred_language,
                 output_directory=None, file_name_prefix=None, xmind_root_node_title=None):
        self.input_directory = None
        self.output_directory = None
        self.namespaces = namespaces
        self.preferred_language = preferred_language
        self.local_namespace = local_namespace
        self.scheme_name = scheme_name
        self.file_name_prefix = None
        self.xmind_root_node_title = xmind_root_node_title

    def xmind_to_rdf(self, xmind_file, rdf_file, xmind_root_node_title=None, sheet_no=0):
        xmindapp = XMind2SKOS(self.local_namespace, self.scheme_name, default_language=self.preferred_language,
                              bindings=self.namespaces)
        xmindapp.read_xmind(xmind_file=xmind_file, rdf_file=rdf_file,
                            sheet_no=sheet_no, xmind_root_node_title=xmind_root_node_title)

    def excel_to_rdf(self, xls_file, rdf_file):
        # Read the Excel file and generate an RDF SKOS file writen to function_ttl_file
        app = XLS2SKOS(self.local_namespace, self.scheme_name, default_language=self.preferred_language,
                       bindings=self.namespaces)
        # level_col: defines the column name of the hierarchy level
        # value_col: defines the column name of the element name
        loaded_scheme = app.read_xls(xls_file, level_col='Level', value_col='Name', note_col='Notes', sheet_number=0)
        app.to_rdf(loaded_scheme, rdf_file)

    def rdf_to_xmind(self, rdf_file, xmind_file):
        # Load function_ttl_file and generate a XMind File from it
        graph = self.read_graph(rdf_file, self.namespaces)
        SKOS2XMind.write(graph, xmind_file, self.preferred_language)

    def rdf_to_excel(self, xls_file, rdf_file):
        graph = self.read_graph(rdf_file, self.namespaces)
        app = SKOS2XLS(preferred_language=self.preferred_language, graph=graph)
        app.write(xls_filename=xls_file)

    def excel_to_xmind(self, xls_file, xmind_file, rdf_file):
        self.excel_to_rdf(xls_file=xls_file, rdf_file=rdf_file)
        self.rdf_to_xmind(rdf_file=rdf_file, xmind_file=xmind_file)

    def xmind_to_excel(self, xmind_file, xls_file, rdf_file, xmind_root_node_title=None):
        if xmind_root_node_title is None:
            xmind_root_node_title = self.xmind_root_node_title

        self.xmind_to_rdf(xmind_file=xmind_file, rdf_file=rdf_file, xmind_root_node_title=xmind_root_node_title)
        self.rdf_to_excel(rdf_file=rdf_file, xls_file=xls_file)

    def rdf_to_ascii(self, rdf_file, ascii_file):
        graph = self.read_graph(rdf_file, self.namespaces)
        app = SKOS2ASCII()
        app.write(graph, pref_lang=self.preferred_language, filename=ascii_file)

    def rdf_to_graphviz(self, rdf_file, dot_file, dot_prolog='',
                        visited_relations=[SKOS.narrower, SKOS.broader],
                        html_nodes=True,
                        html_nodes_with_pref_labels=True,
                        html_nodes_with_rdftype=True):
        graph = self.read_graph(rdf_file, self.namespaces)
        prolog = dot_prolog
        # This is an example of how to pass a tailored function of what label to print
        app = SKOS2GRAPHVIZ(graph, preferred_language=self.preferred_language,
                            prolog_definitions=prolog,
                            label_function=self.hidden_label,
                            visited_relations=visited_relations,
                            html_nodes=html_nodes,
                            html_nodes_with_rdftype=html_nodes_with_rdftype,
                            html_nodes_with_pref_labels=html_nodes_with_pref_labels)
        app.write(graph, filename=dot_file)

    @staticmethod
    def hidden_label(concept, graph, preferred_language):
        lab = graph.hidden_label(concept, preferred_language)
        if lab:
            return lab
        else:
            return graph.pref_label(concept, preferred_language)

    @staticmethod
    def read_graph(rdf_file, namespaces):
        return SKOSGraph(rdf_file, namespaces=namespaces, poor_man_reasoning=True)


@converterApp.command()
def excel_to_xmind(input=None, output=None, rdf_file=None):
    remove_rdf_file = False
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".xlsx")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".xmind")
    if rdf_file is None:
        rdf_file = converter.output_directory + "temp_rdf_file.ttl"
        remove_rdf_file = True
    converter.excel_to_xmind(xls_file=input, xmind_file=output, rdf_file=rdf_file)
    if remove_rdf_file:
        os.remove(rdf_file)


@converterApp.command()
def xmind_to_excel(input=None, output=None, rdf_file=None, xmind_root_node_title=None):
    remove_rdf_file = False
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".xmind")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".xlsx")
    if rdf_file is None:
        rdf_file = converter.output_directory + "temp_rdf_file.ttl"
        remove_rdf_file = True
    converter.xmind_to_excel(xmind_file=input, rdf_file=rdf_file, xls_file=output,
                             xmind_root_node_title=xmind_root_node_title)
    if remove_rdf_file:
        os.remove(rdf_file)


@converterApp.command()
def xmind_to_rdf(input=None, output=None, xmind_root_node_title=None):
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".xmind")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".ttl")
    converter.xmind_to_rdf(xmind_file=input, rdf_file=output, xmind_root_node_title=xmind_root_node_title)


@converterApp.command()
def excel_to_rdf(input=None, output=None):
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".xlsx")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".ttl")

    print("Converting " + input + " to " + output + ".")
    converter.excel_to_rdf(xls_file=input, rdf_file=output)


@converterApp.command()
def rdf_to_xmind(input=None, output=None):
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".ttl")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".xmind")
    converter.rdf_to_xmind(rdf_file=input, xmind_file=output)


@converterApp.command()
def rdf_to_excel(input=None, output=None):
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".ttl")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".xlsx")

    print("Converting " + input + " to " + output + ".")
    converter.rdf_to_excel(rdf_file=input, xls_file=output)


@converterApp.command()
def rdf_to_graphviz(input=None, output=None):
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".ttl")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".dot")
    print("Converting " + input + " to " + output + ".")
    converter.rdf_to_graphviz(rdf_file=input, dot_file=output)


@converterApp.command()
def rdf_to_ascii(input=None, output=None):
    converter = create_converter()
    if input is None:
        input = os.path.join(converter.input_directory, converter.file_name_prefix + ".ttl")
    if output is None:
        output = os.path.join(converter.output_directory, converter.file_name_prefix + ".txt")
    print("Converting " + input + " to " + output + ".")
    converter.rdf_to_ascii(rdf_file=input, ascii_file=output)


if __name__ == "__main__":
    converterApp()
