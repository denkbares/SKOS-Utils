import os
import sys
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent

def activate_venv():
    venv_path = os.environ['VIRTUAL_ENV']
    if sys.platform.startswith("win"):
        activate_this = os.path.join(venv_path, "Scripts", "activate_this.py")
    else:
        activate_this = os.path.join(venv_path, "bin", "activate_this.py")

    exec(compile(open(activate_this, "rb").read(), activate_this, 'exec'), dict(__file__=activate_this))