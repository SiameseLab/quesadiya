import pkg_resources
import os


# version info of this package
__version__ = pkg_resources.get_distribution("quesadiya").version
# root path ../quesadiya
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# projects path ../quesadiya/projects
PROJECT_DIR = os.path.join(BASE_DIR, "projects")


def get_base_path():
    return BASE_DIR


def get_projects_path():
    return PROJECT_DIR
