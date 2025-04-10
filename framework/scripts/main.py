# Standard
import asyncio
import shutil
import argparse

# DCB
from dcb.run.run_test import run_test


async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Run benchmark tests with specified working directory"
    )
    parser.add_argument(
        "-d",
        "--work-dir",
        type=str,
        required=True,
        help="Working directory containing benchmark tests",
    )
    parser.add_argument(
        "-n",
        "--test-name",
        type=str,
        required=True,
        help="Name of the test to run",
    )
    parser.add_argument(
        "-c",
        "--checkpoint-dir",
        type=str,
        required=False,
        help="Checkpoint directory to use for the test",
    )
    args = parser.parse_args()

    await run_test(args.work_dir, args.test_name, args.checkpoint_dir)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError(
            "npx is not installed. Please install it with `npm install -g npx`."
        )

    asyncio.run(main())
