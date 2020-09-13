import pkg_resources
import os


# version info of this package
__version__ = pkg_resources.get_distribution("quesadiya").version
# get root path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def show_path():
    return BASE_DIR
