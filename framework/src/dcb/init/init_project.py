# Standard
import os
import shutil

# DCB
from dcb.common.constants import TEMPLATE_DIR


async def init_project(project_dir: str):
    """Initialize a DCB project directory.

    Args:
        project_dir: The location to initialize the DCB project directory.
    """

    config_dir = os.path.join(project_dir, "config")
    os.makedirs(config_dir, exist_ok=True)

    # Create settings.yaml
    settings_yaml_path = os.path.join(config_dir, "settings.yaml")
    shutil.copy(
        os.path.join(TEMPLATE_DIR, "settings.yaml.template"),
        settings_yaml_path,
    )

    # Create firebase_credentials.yaml
    firebase_credentials_yaml_path = os.path.join(
        config_dir, "firebase_credentials.yaml"
    )
    shutil.copy(
        os.path.join(TEMPLATE_DIR, "firebase_credentials.yaml.template"),
        firebase_credentials_yaml_path,
    )
