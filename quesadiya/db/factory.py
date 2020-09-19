from .interface import SQLAlchemyInterface

from .config import ADMIN_PATH
from .config import CONFIG_ADMINDB
from .config import CONFIG_PROJECTDB
from .config import PROJECTDB_NAME

from .schema import ProjectDB

from sqlalchemy import create_engine

import os


def get_admindb_interface():
    engine = _get_admindb_engine(db_path=ADMIN_PATH)
    interface = SQLAlchemyInterface(engine=engine)
    return interface


def get_projectdb_interface(db_dir_path):
    engine = _get_projectdb_engine(db_dir_path=db_dir_path)
    interface = SQLAlchemyInterface(engine=engine)
    return interface


def init_projectdb(db_dir_path):
    engine = _get_projectdb_engine(db_dir_path=db_dir_path)
    ProjectDB.Base.metadata.create_all(engine)


def _get_admindb_engine(db_path):
    return _get_engine(db_path, CONFIG_ADMINDB)


def _get_projectdb_engine(db_dir_path):
    db_path = os.path.join(db_dir_path, PROJECTDB_NAME)
    return _get_engine(db_path, CONFIG_PROJECTDB)


def _get_engine(db_path, config):
    db_uri = 'sqlite:///' + db_path
    return create_engine(db_uri, **config)
