import yaml


def load_config(config_path: str = "./../config.yaml"):  # todo
    with open(config_path) as fd:
        config = yaml.safe_load(fd)

    return config
