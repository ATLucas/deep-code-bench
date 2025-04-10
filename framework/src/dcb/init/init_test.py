# Standard
import os
import shutil

# DCB
from dcb.init.init_firebase_react_app import init_firebase_react_app


async def init_test(
    working_dir: str, test_name: str, checkpoint_dir: str = None
) -> str:
    # Create the test directory if it doesn't exist
    working_dir = os.path.abspath(working_dir)
    test_dir = os.path.join(working_dir, test_name)

    print(f"Created benchmark test directory: {test_dir}")

    if checkpoint_dir:
        # Copy the checkpoint directory to the test directory
        shutil.copytree(checkpoint_dir, test_dir)
        print(f"Copied checkpoint directory: {checkpoint_dir} to {test_dir}")
    else:
        # Initialize the test directory
        await init_firebase_react_app(test_dir)

    return test_dir
