import pkg_resources
import os


# version info of this package
# __version__ = pkg_resources.get_distribution("quesadiya").version
# root path ../quesadiya
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# projects path ../quesadiya/projects
PROJECT_DIR = os.path.join(BASE_DIR, "projects")


def get_base_path():
    return BASE_DIR


def get_projects_path():
    return PROJECT_DIR


# init admin.db if it doesn't exist
admin_path = os.path.join(PROJECT_DIR, "admin.db")
if not os.path.exists(admin_path):
    from quesadiya.init_admin import init_admin
    init_admin()
