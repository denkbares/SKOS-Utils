from unittest import TestCase
import os
import sys

# sys.path.append(os.path.join(os.path.abspath("../SKOSTools/TSAConverter"), "SKOSUtils"))
# sys.path.append(os.path.abspath("../SKOSTools/TSAConverter/SKOSUtils"))
sys.path.append(os.path.join(os.path.abspath(".."), "SKOSUtils"))


import filecmp
import pandas
import pandas as pd
from rdflib import Namespace
import xmind
import re
from pathlib import Path

from SKOSTools.TSAConverter.TSAConverter import TSAConverter


# Returns true, if both xls-files have the save entries
def compare_excel_files(original_xls_file, test_xls_file, print_differences):
    # NaN = NaN -> false, but should be true ("NaNs in the same location are considered equal."
    #  -> https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.equals.html)
    # Therefore filling NaN cells with ''
    original_xls_file = pd.read_excel(original_xls_file).fillna('')
    test_xls_file = pd.read_excel(test_xls_file).fillna('')

    original_xls_file.equals(test_xls_file)

    comparison_values = original_xls_file.values == test_xls_file.values
    if print_differences:
        print(comparison_values)
    return all(all(row) for row in comparison_values)


def compare_rdf_files(original_rdf_file, test_rdf_file, print_differences):
    print("Comparing file " + original_rdf_file + " with " + test_rdf_file)
    original_file = open(original_rdf_file)
    test_file = open(test_rdf_file)

    # Whole document comparison
    files_are_equal = filecmp.cmp(original_rdf_file, test_rdf_file)

    # closing files
    original_file.close()
    test_file.close()
    return files_are_equal


# Compare tags "level", "order" and "prefLabel"
# Compare broader and narrower
def compare_rdf_files_content(original_rdf_file, test_rdf_file, print_differences):
    original_txt = Path(original_rdf_file).read_text('utf-8')
    test_txt = Path(test_rdf_file).read_text('utf-8')
    single_concept_pattern = "<http://www.denkbares.com/casis#[<>;\"@,\\s\\/\\.:\\d\\w\u00c4-\u00fc\u00df#]+?(?=\n\n<)"

    # First get a list of all concepts, then get label, level, order
    concept_list_original = re.findall(single_concept_pattern, original_txt)
    concept_list_test = re.findall(single_concept_pattern, test_txt)

    original_df = create_dataframe_from_concepts(concept_list_original)
    test_df = create_dataframe_from_concepts(concept_list_test)

    # Compare label, level and "order in relation". Therefor match broader-siblings and compare the order.
    comparison_df = pd.DataFrame.compare(test_df, original_df)

    if print_differences:
        print(comparison_df)
        # print(test_df)
        # print(original_df)

    # Test if labels and their order are equal
    return pd.DataFrame.equals(test_df.Label, original_df.Label)


def create_dataframe_from_concepts(concept_list):
    id_list_pattern = "(?<=<http://www.denkbares.com/casis#)[\\d\\w]*(?=>)"
    level_pattern = "(?<=level:\\s)\\d*"
    order_pattern = "(?<=order:\\s)\\d*"
    # Add German "Umlaute" Ä, Ö, Ü
    pref_label_pattern = "(?<=prefLabel\\s\")[\\w\u00c4-\u00fc\u00df]*(?=\")"
    broader_pattern = "(?<=broader\\s<http://www.denkbares.com/casis#)[\\d\\w]*(?=>)"

    id_list = extract_from_concepts(concept_list, id_list_pattern, "")
    label_list = extract_from_concepts(concept_list, pref_label_pattern, 'prefLabel')
    level_list = extract_from_concepts(concept_list, level_pattern, 'level :')
    order_list = extract_from_concepts(concept_list, order_pattern, 'order :')
    dataframe = pandas.DataFrame(list(zip(id_list, label_list, level_list, order_list)),
                                 columns=['ID', 'Label', 'Level', 'Order'])

    broader_list = extract_from_concepts(concept_list, broader_pattern, '<http://www.denkbares.com/casis#')
    broader_label_list = []
    for i in broader_list:
        temp_label = dataframe.loc[dataframe['ID'] == i]['Label']
        if temp_label.size > 0:
            broader_label_list.append(temp_label.values[0])
        else:
            broader_label_list.append("")

    dataframe.Order = dataframe.Order.astype(int)
    dataframe.Level = dataframe.Level.astype(int)

    # Add Broader column
    dataframe["Broader"] = broader_label_list
    # Sort by broader and by order
    dataframe = dataframe.sort_values(by=['Broader', 'Order'], ignore_index=True)

    return dataframe


# Extracts the pattern from the concept and removes the substring
def extract_from_concepts(concept_list, pattern, substring):
    strings = [re.findall(pattern, concept) for concept in concept_list]

    for i in range(len(strings)):
        if len(strings[i]) > 0:
            strings[i] = strings[i][0]
        else:
            strings[i] = ""

    # result = [s.replace(substring, '') for s in strings]
    return strings


class TestConverter(TestCase):
    def setUp(self):
        # print("Setting up test environment...")

        local_namespace = Namespace('http://www.denkbares.com/casis#')
        namespaces = {'http://www.claas.com/casis#': 'cl'}
        scheme_name = 'Functions'
        preferred_language = 'de'
        self.test_converter = TSAConverter(namespaces, local_namespace, scheme_name, preferred_language)

        out_dir = '../data/Testdata/'

        # Original files
        self.original_xls_file = out_dir + 'Bike_Testdata_Original.xlsx'
        self.original_rdf_file = out_dir + 'Bike_Testdata_Original.ttl'
        self.original_xmind_file = out_dir + 'Bike_Testdata_Original.xmind'

        # Wrong Original files
        self.original_xls_file_wrong = out_dir + 'Bike_Testdata_Original_Wrong.xlsx'
        self.original_rdf_file_wrong = out_dir + 'Bike_Testdata_Original_Wrong.ttl'
        self.original_xmind_file_wrong = out_dir + 'Bike_Testdata_Original_Wrong.xmind'

        self.xls_file = out_dir + 'Bike_Testdata.xlsx'
        self.rdf_file = out_dir + 'Bike_Testdata.ttl'
        self.xmind_file = out_dir + 'Bike_Testdata.xmind'
        self.xls_filename_temp = out_dir + 'deleteMe.xlsx'
        self.xmind_root_node_title = 'Bike'

        # print("Finish setting up test environment!")

    def test_xmind_to_rdf(self):
        self.test_converter.xmind_to_rdf(xmind_file=self.original_xmind_file, rdf_file=self.rdf_file,
                                         xmind_root_node_title=self.xmind_root_node_title)
        self.assertTrue(compare_rdf_files_content(self.original_rdf_file, self.rdf_file, False),
                        "There are differences in the files.")
        # self.assertFalse(compare_rdf_files_content(self.original_rdf_file_wrong, self.rdf_file, False))

    def test_xls_to_rdf(self):
        # print("Testing xls to rdf function...")
        self.test_converter.excel_to_rdf(xls_file=self.original_xls_file, rdf_file=self.rdf_file)

        self.assertTrue(compare_rdf_files_content(self.original_rdf_file, self.rdf_file, False),
                        "There are differences in the files.")
        # self.assertFalse(compare_rdf_files_content(self.original_rdf_file_wrong, self.rdf_file, False))
        # print("Testing xls to rdf function completed!")

    def test_rdf_to_xmind(self):
        self.test_converter.rdf_to_xmind(rdf_file=self.original_rdf_file, xmind_file=self.xmind_file)

        original_file = xmind.load(self.original_xmind_file)
        test_file = xmind.load(self.xmind_file)

        # TODO: Compare xmind-files
        # original_file.

    def test_rdf_to_excel(self):
        self.test_converter.rdf_to_excel(rdf_file=self.original_rdf_file, xls_file=self.xls_file)

        self.assertTrue(compare_excel_files(self.original_xls_file, self.xls_file, False))

    def test_xls_to_xmind(self):
        self.test_converter.excel_to_xmind(xls_file=self.original_xls_file, xmind_file=self.xmind_file,
                                           rdf_file=self.rdf_file)

        original_file = xmind.load(self.original_xmind_file)
        test_file = xmind.load(self.xmind_file)

        # TODO: Compare xmind-files
        # original_file.

    def test_xmind_to_excel(self):
        self.test_converter.xmind_to_excel(xmind_file=self.original_xmind_file, rdf_file=self.rdf_file,
                                           xls_file=self.xls_file,
                                           xmind_root_node_title=self.xmind_root_node_title)
        self.assertTrue(compare_excel_files(self.original_xls_file, self.xls_file, False))
        # self.assertFalse(compare_excel_files(self.original_xls_file_wrong, self.xls_file, False))
