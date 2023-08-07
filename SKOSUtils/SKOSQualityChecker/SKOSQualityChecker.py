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
from SKOSUtils import Utils
import time

from SKOSUtils.UtilDir.SKOSGraph import SKOSGraph

Utils.activate_venv()
sys.path.append(os.path.abspath("../../../SKOSUtils"))


class SKOSQualityChecker:

    def __init__(self):
        self.config = None

    def run_test(self, test_name, graph):
        # import the module containing the test class
        checker_module = 'SKOSUtils.SKOSQualityChecker.CheckerModules.'
        test_module = importlib.import_module(checker_module + test_name)
        test_class = getattr(test_module, test_name)
        test = test_class()
        return test.execute(graph, self.config['logging'])

    def main(self):

        if args.config:
            config_path = args.config
        else:
            config_path = os.path.join('configs', 'SKOSQualityChecker_config.yaml')
            print("Using default config.")

        with open(config_path) as f:
            self.config = yaml.load(f, Loader=SafeLoader)

        # Get input file name from argument or config file if existing
        if args.graph:
            input_file = args.graph
            print("Input file \"" + input_file + "\" selected with \"-graph\" argument.")
        elif "input" in self.config:
            input_file = self.config["input"]
            print("Input file \"" + input_file + "\" selected with config file \"" + config_path + "\" .")
        else:
            input_file = "tests/Testdata/SKOS_Checker_Debug_File.ttl"
            print("Using default input file.")

        if self.config['logging']:
            if 'log_file' in self.config:
                log_file = self.config['log_file']
            else:
                log_file = 'SKOSQualityChecker.log'
            logging.basicConfig(filename=log_file, filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO)

        logging.info('Open SKOS file [' + input_file + ']')
        graph = rdflib.Graph()
        graph.parse(input_file, format='turtle')
        graph = SKOSGraph.poor_man_reasoning(graph)
        logging.info('SKOS file parsed')

        # Read the selected tests from a config file and only run those
        selected_tests = self.config["tests"]
        logging.info(str(len(selected_tests)) + " checks selected.")

        result_df_list = []
        benchmark_list = []

        for test_name in selected_tests:
            print("Running " + test_name + ".")
            logging.info("Running " + test_name + ".")
            start_time = time.time()
            result_df = self.run_test(test_name, graph)
            end_time = time.time()
            elapsed_time = self.format_duration(end_time - start_time)

            result_df_list.append(result_df)
            benchmark_result = [test_name, elapsed_time, len(result_df)]
            benchmark_list.append(benchmark_result)
        logging.info('Checks finished.')

        final = pd.concat(result_df_list, ignore_index=True)
        benchmark_df = pd.DataFrame(columns=['CheckName', 'Time', 'Findings'], data=benchmark_list)

        print(benchmark_df)

        # Set date and time string to concat to output file name
        now = ""
        if self.config["add_datetime_to_output_file"]:
            now = datetime.now().strftime('%Y-%m-%d_%H-%M')

        if "output" in self.config:
            output_file = self.config["output"] + now + ".xlsx"
        else:
            output_file = f'test_results_{now}.xlsx'

        # export dataframe to excel
        if self.config["write_results_to_excel"]:
            # final.to_excel(output_file)
            with pd.ExcelWriter(output_file) as writer:
                final.to_excel(writer, sheet_name='Checker_Results')
                benchmark_df.to_excel(writer, sheet_name='Checker_Benchmark')
        logging.info('Idle.')

    @staticmethod
    def format_duration(seconds):
        round_seconds = round(seconds, 3)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        milliseconds = int((round_seconds - int(round_seconds)) * 1000)

        duration_string = "{:02d}:{:02d}:{:02d}:{:03d}".format(int(hours), int(minutes), int(seconds), int(milliseconds))
        return duration_string


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script checks the structure of a given SKOS vocabulary.")
    parser.add_argument("-config", required=False, help="Configuration of SKOSQualityChecker in yaml-format")
    parser.add_argument("-graph", required=False, help="Graph to be checked")

    app = SKOSQualityChecker()
    args = parser.parse_args()
    app.main()
