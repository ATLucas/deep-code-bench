# Standard
import os


FRAMEWORK_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
ROOT_DIR = os.path.dirname(FRAMEWORK_DIR)
TEMPLATE_DIR = os.path.join(FRAMEWORK_DIR, "templates")
