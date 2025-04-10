# Standard
import asyncio
import shutil
import argparse

# DCB
from dcb.init.init_project import init_project


async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Initialize a DCB project directory")
    parser.add_argument(
        "-p",
        "--project-dir",
        type=str,
        required=True,
        help="Project directory",
    )
    args = parser.parse_args()

    await init_project(args.project_dir)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError(
            "npx is not installed. Please install it with `npm install -g npx`."
        )

    asyncio.run(main())
