# Standard
import os
import shutil

# DCB
from dcb.common.config import parse_config
from dcb.common.constants import TEMPLATE_DIR


async def init_project_app(project_dir: str):
    """Initialize a Firebase React app in the given directory.

    Args:
        project_dir: The location to initialize the Firebase React app.
    """

    project_app_dir = os.path.join(project_dir, "app")

    # Load settings
    settings = parse_config(os.path.join(project_dir, "config", "settings.yaml"))

    # Copy the template directory to the given directory
    shutil.copytree(
        os.path.join(TEMPLATE_DIR, "firebase_react_starter"), project_app_dir
    )

    # Replace the template values with the given values
    replace_in_file(
        os.path.join(project_app_dir, "package.json"),
        "some-react-app-name",
        settings["react_app_name"],
    )
    replace_in_file(
        os.path.join(project_app_dir, ".firebaserc"),
        "some-firebase-project-name",
        settings["firebase_project_name"],
    )
    for relative_path in ["public/index.html", "public/manifest.json"]:
        replace_in_file(
            os.path.join(project_app_dir, relative_path),
            "some-web-app-name",
            settings["web_app_name"],
        )
        replace_in_file(
            os.path.join(project_app_dir, relative_path),
            "some-web-app-description",
            settings["web_app_description"],
        )

    # Load firebase credentials yaml
    firebase_creds = parse_config(
        os.path.join(project_dir, "config", "firebase_credentials.yaml")
    )

    for env_file in [
        ".env.development.local",
        ".env.development.local.prod",
        ".env.development.local.test",
        ".env.production.local",
    ]:
        with open(
            os.path.join(project_app_dir, env_file),
            "w",
        ) as file:
            file.write("REACT_APP_FIREBASE_API_KEY=" + firebase_creds["apiKey"] + "\n")
            file.write(
                "REACT_APP_FIREBASE_AUTH_DOMAIN=" + firebase_creds["authDomain"] + "\n"
            )
            file.write(
                "REACT_APP_FIREBASE_PROJECT_ID=" + firebase_creds["projectId"] + "\n"
            )
            file.write(
                "REACT_APP_FIREBASE_STORAGE_BUCKET="
                + firebase_creds["storageBucket"]
                + "\n"
            )
            file.write(
                "REACT_APP_FIREBASE_MESSAGING_SENDER_ID="
                + firebase_creds["messagingSenderId"]
                + "\n"
            )
            file.write("REACT_APP_FIREBASE_APP_ID=" + firebase_creds["appId"] + "\n")
            file.write(
                "REACT_APP_FIREBASE_MEASUREMENT_ID="
                + firebase_creds["measurementId"]
                + "\n"
            )


def replace_in_file(file_path: str, old: str, new: str):
    with open(file_path, "r") as file:
        content = file.read()
    content = content.replace(old, new)
    with open(file_path, "w") as file:
        file.write(content)
