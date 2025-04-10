# Standard
import yaml


def parse_config(config_path: str) -> dict:
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
