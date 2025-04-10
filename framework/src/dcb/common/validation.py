# Standard
import os


def is_valid_project_dir(project_dir: str) -> bool:
    return os.path.exists(os.path.join(project_dir, "config", "settings.yaml"))
