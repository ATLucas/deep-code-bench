# Standard
import asyncio
import shutil
import argparse
import os

# DCB
from dcb.init.init_firebase_react_app import init_firebase_react_app


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

    # Check if the project directory exists
    if not os.path.exists(args.project_dir):
        raise FileNotFoundError(f"Project directory {args.project_dir} does not exist")

    # Check if the project directory is a DCB project directory
    if not os.path.exists(os.path.join(args.project_dir, "config", "settings.yaml")):
        raise FileNotFoundError(
            f"Project directory {args.project_dir} is not a DCB project directory"
        )

    await init_firebase_react_app(args.project_dir)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError(
            "npx is not installed. Please install it with `npm install -g npx`."
        )

    asyncio.run(main())
