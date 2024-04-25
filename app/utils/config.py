import os.path
from pathlib import Path

import yaml

root_dir = Path(__file__).parent.parent.parent

CONFIG_FILE_NAME = "config.yaml"


def load_config(config_path: str = os.path.join(root_dir, CONFIG_FILE_NAME)):
    with open(config_path) as fd:
        config = yaml.safe_load(fd)

    return config
