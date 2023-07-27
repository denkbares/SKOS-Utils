import yaml
from yaml import SafeLoader
from SKOSUtils.SKOSQualityChecker.SKOSQualityChecker import SKOSQualityChecker


# An example checking for cyclic broader/narrower relations
with open('examples/Cyclic_checker_config.yaml') as f:
    config_data = yaml.load(f, Loader=SafeLoader)
# Get input file name from config file if existing
if "input" in config_data:
    input_file = config_data["input"]
    app = SKOSQualityChecker(config=config_data)
    app.main(input_file)


# An example checking a larger range of checks
with open('examples/TestBike_checker_config.yaml') as f:
    config_data = yaml.load(f, Loader=SafeLoader)
# Get input file name from config file if existing
if "input" in config_data:
    input_file = config_data["input"]
    app = SKOSQualityChecker(config=config_data)
    app.main(input_file)
