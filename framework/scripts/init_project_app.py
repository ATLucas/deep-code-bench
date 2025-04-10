# Standard
import asyncio
import shutil
import argparse
import os

# DCB
from dcb.common.constants import ROOT_DIR
from dcb.common.validation import is_valid_project_dir
from dcb.init_project.init_app import init_project_app


async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Initialize a Firebase React app in the given directory"
    )
    parser.add_argument(
        "-p",
        "--project-dir",
        type=str,
        required=True,
        help="Project directory",
    )
    args = parser.parse_args()

    project_dir = os.path.abspath(os.path.join(ROOT_DIR, args.project_dir))

    if not is_valid_project_dir(project_dir):
        raise ValueError(
            f"Project directory {project_dir} is not a valid DCB project directory"
        )

    await init_project_app(project_dir)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError(
            "npx is not installed. Please install it with `npm install -g npx`."
        )

    asyncio.run(main())
