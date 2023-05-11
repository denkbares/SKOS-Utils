import os

from SKOSTools import Utils

from SKOSTools.TSAConverter.SKOSUtils.SKOS2XLS import SKOS2XLS
from SKOSTools.TSAConverter.SKOSUtils.SKOS2XMind import SKOS2XMind
from SKOSTools.TSAConverter.SKOSUtils.SKOSGraph import SKOSGraph
from SKOSTools.TSAConverter.SKOSUtils.XLS2SKOS import XLS2SKOS
from SKOSTools.TSAConverter.SKOSUtils.XMind2SKOS import XMind2SKOS

root_path = Utils.get_project_root()
activate_this_file = os.path.join(root_path, "venv", "Scripts", "activate_this.py")

exec(compile(open(activate_this_file, "rb").read(), activate_this_file, 'exec'), dict(__file__=activate_this_file))

from rdflib import Namespace
import typer
import yaml
from yaml.loader import SafeLoader

converterApp = typer.Typer()


def create_converter():
    # Open the file and load the file
    with open('../../configs/TSAConverter_config.yaml') as f:
        config_data = yaml.load(f, Loader=SafeLoader)
    # define the namespace, in which the newly generated concepts are located
    local_namespace = Namespace(config_data["nameSpace"])
    namespaces = {config_data["nameSpace"]: config_data["nameSpaceKey"]}
    scheme_name = config_data["schemeName"]
    preferred_language = config_data["preferredLanguage"]

    result_converter = TSAConverter(namespaces, local_namespace, scheme_name, preferred_language)

    if "outputDirectory" in config_data:
        result_converter.output_directory = config_data["outputDirectory"]
    else:
        result_converter.output_directory = ""
    if "fileNamePrefix" in config_data:
        result_converter.file_name_prefix = config_data["fileNamePrefix"]
    else:
        result_converter.file_name_prefix = "SKOSUtils/tempFile"
    if "xMindRootTitle" in config_data:
        result_converter.xmind_root_node_title = config_data["xMindRootTitle"]
    else:
        result_converter.xmind_root_node_title = None

    return result_converter


class TSAConverter:
    def __init__(self, namespaces, local_namespace, scheme_name, preferred_language,
                 output_directory=None, file_name_prefix=None, xmind_root_node_title=None):
        self.namespaces = namespaces
        self.preferred_language = preferred_language
        self.local_namespace = local_namespace
        self.scheme_name = scheme_name
        self.output_directory = None
        self.file_name_prefix = None
        self.xmind_root_node_title = xmind_root_node_title

    def xmind_to_rdf(self, xmind_file, rdf_file, xmind_root_node_title=None):
        if xmind_root_node_title is None:
            xmind_root_node_title = self.xmind_root_node_title
        xmindapp = XMind2SKOS(self.local_namespace, self.scheme_name, default_language=self.preferred_language,
                              bindings=self.namespaces)
        xmindapp.read_xmind(xmind_file=xmind_file, rdf_file=rdf_file,
                            sheet_no=1, xmind_root_node_title=xmind_root_node_title)

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
        graph = SKOSGraph(rdf_file, self.namespaces)
        SKOS2XMind.write(graph, xmind_file, self.preferred_language)

    def rdf_to_excel(self, xls_file, rdf_file):
        graph = SKOSGraph(rdf_file, self.namespaces)
        app = SKOS2XLS(prefered_language='de', graph=graph)
        app.write(xls_filename=xls_file)

    def excel_to_xmind(self, xls_file, xmind_file, rdf_file):
        self.excel_to_rdf(xls_file=xls_file, rdf_file=rdf_file)
        self.rdf_to_xmind(rdf_file=rdf_file, xmind_file=xmind_file)

    def xmind_to_excel(self, xmind_file, xls_file, rdf_file, xmind_root_node_title=None):
        if xmind_root_node_title is None:
            xmind_root_node_title = self.xmind_root_node_title

        self.xmind_to_rdf(xmind_file=xmind_file, rdf_file=rdf_file, xmind_root_node_title=xmind_root_node_title)
        self.rdf_to_excel(rdf_file=rdf_file, xls_file=xls_file)


@converterApp.command()
def excel_to_xmind(xls_file=None, xmind_file=None, rdf_file=None):
    remove_rdf_file = False
    converter = create_converter()
    if xls_file is None:
        xls_file = converter.output_directory + converter.file_name_prefix + ".xlsx"
    if xmind_file is None:
        xmind_file = converter.output_directory + converter.file_name_prefix + ".xmind"
    if rdf_file is None:
        rdf_file = converter.output_directory + "temp_rdf_file.ttl"
        remove_rdf_file = True
    converter.excel_to_xmind(xls_file=xls_file, xmind_file=xmind_file, rdf_file=rdf_file)
    if remove_rdf_file:
        os.remove(rdf_file)


@converterApp.command()
def xmind_to_excel(xmind_file=None, xls_file=None, rdf_file=None, xmind_root_node_title=None):
    remove_rdf_file = False
    converter = create_converter()
    if xls_file is None:
        xls_file = converter.output_directory + converter.file_name_prefix + ".xlsx"
    if xmind_file is None:
        xmind_file = converter.output_directory + converter.file_name_prefix + ".xmind"
    if rdf_file is None:
        rdf_file = converter.output_directory + "temp_rdf_file.ttl"
        remove_rdf_file = True
    converter.xmind_to_excel(xmind_file=xmind_file, rdf_file=rdf_file, xls_file=xls_file,
                             xmind_root_node_title=xmind_root_node_title)
    if remove_rdf_file:
        os.remove(rdf_file)


@converterApp.command()
def xmind_to_rdf(xmind_file=None, rdf_file=None, xmind_root_node_title=None):
    converter = create_converter()
    if xmind_file is None:
        xmind_file = converter.output_directory + converter.file_name_prefix + ".xmind"
    if rdf_file is None:
        rdf_file = converter.output_directory + converter.file_name_prefix + ".ttl"
    converter.xmind_to_rdf(xmind_file=xmind_file, rdf_file=rdf_file, xmind_root_node_title=xmind_root_node_title)


@converterApp.command()
def excel_to_rdf(xls_file=None, rdf_file=None):
    converter = create_converter()
    if xls_file is None:
        xls_file = converter.output_directory + converter.file_name_prefix + ".xlsx"
    if rdf_file is None:
        rdf_file = converter.output_directory + converter.file_name_prefix + ".ttl"

    print("Converting " + xls_file + " to " + rdf_file + ".")
    converter.excel_to_rdf(xls_file=xls_file, rdf_file=rdf_file)


@converterApp.command()
def rdf_to_xmind(rdf_file=None, xmind_file=None):
    converter = create_converter()
    if rdf_file is None:
        rdf_file = converter.output_directory + converter.file_name_prefix + ".ttl"
    if xmind_file is None:
        xmind_file = converter.output_directory + converter.file_name_prefix + ".xmind"
    converter.rdf_to_xmind(rdf_file=rdf_file, xmind_file=xmind_file)


@converterApp.command()
def rdf_to_excel(rdf_file=None, xls_file=None):
    converter = create_converter()
    if rdf_file is None:
        rdf_file = converter.output_directory + converter.file_name_prefix + ".ttl"
    if xls_file is None:
        xls_file = converter.output_directory + converter.file_name_prefix + ".xlsx"

    print("Converting " + rdf_file + " to " + xls_file + ".")
    converter.rdf_to_excel(rdf_file=rdf_file, xls_file=xls_file)


if __name__ == "__main__":
    converterApp()
