import os
from setuptools import setup

# Get the path to the requirements.txt file
requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")

# Read the requirements.txt file
with open(requirements_path, "r") as f:
    requirements = f.read().splitlines()

# Setup configuration
setup(
    name="SKOS-Utils",
    version="0.1",
    install_requires=requirements,
)
