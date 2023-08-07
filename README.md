# SKOS-Utils

## Introduction
We introduce the tool suite SKOS-Utils for the development and quality assessment of SKOS vocabularies
(Simple Knowledge Organisation System). SKOS is a wide-spread standard for organizing hierarchical
knowledge structures, that uses RDF as basic data model. SKOS-Utils provides converters for spreadsheets
and mindmaps in order to facilitate the bottom-up development of SKOS vocabularies. A suite of quality
checks is used for testing the created vocabularies.

## Project Structure
The main files of this project are located in the SKOSUtils directory. Here you can find the SKOSConverter-file, which
includes functions to convert different data formats. You can simply switch between the well-known RDF syntax 
definitions XML, Turtle, and JSON-LD. The suite provides scripts to bridge this data model from/to the mindmapping
application XMind, to Graphviz, and from/to the spreadsheet application MS-Excel.

You can also find the SKOSQualityChecker in the directory of the same name. For the quality assessment a suite of 
configurable checks is executed as a pipeline. The results for each check are collected and reported after finishing 
the entire pipeline.

[TODO] QuickRDFConverter
[TODO] PoorMansReasoning

In the configs directory you can write your own configs to personalize the modules of this project.

## How to Start
Before you start, make sure to install all required python packages (see `requirements.txt`). After this set the 
working directory to the root directory of this project. 
If you want to test, if everything is set up correctly, you can run `ConverterExample` and `CheckerExample` in the 
example directory.

### Converter
To use the converter, simple specify the converter and input and output file and run the main-function of the 
SKOSConverter.
For example:
```excel-to-rdf --input "D:/SKOSUTILS/Tests/TestData.xlsx" --output "D:/SKOSUTILS/Tests/TestData.ttl"```

You can also use a YAML-config-file to set your settings permanently.

### SKOS Quality Checker
To use the SKOS Quality Checker, you need to specify the path to the graph you want to check. 
Another parameter is the config-file you maybe want to use.
For example:
```-config "configs\SKOSQualityChecker_config2.yaml" -graph "tests/Testdata/Bike_Testdata.ttl"```

In this YAML-config-file you can set your settings permanently and choose advanced options for result outputs
and set up the checker modules for your checker pipeline.

## Advanced Settings
The settings in the charts below can be changed in the respective config file.
### Converter
| Setting name       | Description                                                             |
|--------------------|-------------------------------------------------------------------------|
| input_directory    | Directory of your input file                                            |
| output_directory   | Directory where the output file will be created                         |
| file_name_prefix   | You can set a name prefix if you use the same name for all file formats |
| name_space         | Name space in your knowledge graph                                      |
| name_space_key     | The key of your name space                                              |
| scheme_name        | Name of your scheme                                                     |
| preferred_language | The preferred language of your knowledge graph                          |
| xMind_root_title   | Set the root node title of your xMind graph                             |

### SKOS Quality Checker
| Setting name                | Description                                                                           |
|-----------------------------|---------------------------------------------------------------------------------------|
| input                       | Directory of your input file                                                          |
| output                      | Directory of your output file                                                         |
| add_datetime_to_output_file | Writes the current time and date at the end of your output file                       |
| write_results_to_excel      | Creates an excel file if True, otherwise results are only shown on the console output |
| logging                     | Creates a log file if True                                                            |
| log_file                    | Specify the location and name of the used log file                                    |
| tests                       | Create a test pipeline by writing all tests you want the SKOS Quality Checker to use  |

## Extend this Tool
If you want to extend the quality checks of SKOS-graphs, you can write new checker modules in rdf or SPARQL.
Create the checker file and add your check to your YAML-config-file.
Inherit from the class `StructureTestInterfaceNavigate` or `StructureTestInterfaceSPARQL` and set the status flag and
the result message. Finally, implement the method `find_concepts` or the query to filter all wanted concepts from the given
SKOS-graph. If you are using `StructureTestInterfaceNavigate`, your `find_concepts` method should return a set of 
concepts.