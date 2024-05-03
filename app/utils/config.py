import os.path
from pathlib import Path
from utils.logger import get_logger
import yaml

logger = get_logger(__name__)

root_dir = Path(__file__).parent.parent.parent

CONFIG_FILE_NAME = "config.yaml"


def load_config(config_path: str):
    with open(config_path) as fd:
        config = yaml.safe_load(fd)

    return config


def read_config(category: str, key: str, default: str = None, config_path: str = os.path.join(root_dir, CONFIG_FILE_NAME)):
    try:
        res = load_config(config_path)[category][key]
    except Exception as e:
        logger.error(f"Could not read_config with {category=} and {key=}, error: {e}")
        return default

    return res

