from .interface import SQLAlchemyInterface
from .config import ADMIN_PATH


def get_interface():
    interface = SQLAlchemyInterface(db_path=ADMIN_PATH)
    return interface
