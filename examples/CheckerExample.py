import yaml
from yaml import SafeLoader
from SKOSUtils.SKOSQualityChecker.SKOSQualityChecker import SKOSQualityChecker


# An example checking for cyclic broader/narrower relations
# First load the YAML configuration file
with open('examples/Cyclic_checker_config.yaml') as f:
    config_data = yaml.load(f, Loader=SafeLoader)
# Run checks, when input is known
if "input" in config_data:
    input_file = config_data["input"]
    app = SKOSQualityChecker(config=config_data)
    app.main(input_file)


# An example checking a larger range of checks
# First load the YAML configuration file
with open('examples/TestBike_checker_config.yaml') as f:
    config_data = yaml.load(f, Loader=SafeLoader)
# Run checks, when input is known
if "input" in config_data:
    input_file = config_data["input"]
    app = SKOSQualityChecker(config=config_data)
    app.main(input_file)
