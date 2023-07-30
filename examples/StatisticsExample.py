import yaml
from yaml import SafeLoader

from SKOSUtils.SKOSQualityChecker.SKOSStatistics import SKOSStatistics

# First run YAML configuration file
with open('examples/Statistics_config.yaml') as f:
    stats_config = yaml.load(f, Loader=SafeLoader)

# Execute the statistics runner
app = SKOSStatistics(stats_config)
stats = app.compute_statistics()
app.write(stats, stats_config['output'])
