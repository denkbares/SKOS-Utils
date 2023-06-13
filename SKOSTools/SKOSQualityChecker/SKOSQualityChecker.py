import argparse
import importlib
import logging
import os
import sys
import rdflib
import pandas as pd
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
from SKOSTools import Utils

Utils.activate_venv()
sys.path.append(os.path.abspath("../../../SKOSTools/SKOSTools"))


class SKOSQualityChecker:

    def __init__(self, config):
        self.config = config

    @staticmethod
    def run_test(test_name, graph):
        # import the module containing the test class
        test_module = importlib.import_module("CheckerModules." + test_name)

        test_class = getattr(test_module, test_name)
        test = test_class()
        return test.execute(graph)

    def main(self, file_name):
        if self.config['logging']:
            if 'log_file' in self.config:
                log_file = self.config['log_file']
            else:
                log_file = 'SKOSQualityChecker.log'
            logging.basicConfig(filename=log_file, filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO)

        logging.info('Open SKOS file.')
        graph = rdflib.Graph()
        graph.parse(file_name, format='turtle')
        logging.info('SKOS file parsed.')

        # Read the selected tests from a config file and only run those
        selected_tests = config_data["tests"]
        print(str(len(selected_tests)) + " tests selected:")

        result_df_list = []
        for test_name in selected_tests:
            print("Running " + test_name + ".")
            logging.info("Running " + test_name + ".")
            result_df = self.run_test(test_name, graph)
            result_df_list.append(result_df)

        final = pd.concat(result_df_list, ignore_index=True)
        print(final)

        # Set date and time string to concat to output file name
        now = ""
        if config_data["add_datetime_to_output"]:
            now = datetime.now().strftime('%Y-%m-%d_%H-%M')

        if "output" in config_data:
            output_file = config_data["output"] + now + ".xlsx"
        else:
            output_file = f'test_results_{now}.xlsx'

        # export dataframe to excel
        if config_data["write_results_to_excel"]:
            final.to_excel(output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script checks the structure of the graph in a given RDF-file.")

    with open('configs/SKOSQualityChecker_config.yaml') as f:
        config_data = yaml.load(f, Loader=SafeLoader)

    # Get input file name from config file if existing
    if "input" in config_data:
        input_file = config_data["input"]
    else:
        args = parser.parse_args()
        input_file = args.input
    parser.add_argument("input")

    app = SKOSQualityChecker(config=config_data)
    app.main(input_file)
