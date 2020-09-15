from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .session import SessionContextManager
from .config import CONFIG_ADMINDB

from .schema import Project, Collaborator


def _get_sqlite_engine(db_path):
    db_uri = 'sqlite:///' + db_path
    return create_engine(db_uri, **CONFIG_ADMINDB)


class SQLAlchemyInterface:
    """Execute sql operations in sqlalchemy."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.engine = _get_sqlite_engine(db_path)
        session_maker = sessionmaker(bind=self.engine)
        self.session_context_manager = SessionContextManager(session_maker)

    def get_all_project(self):
        with self.session_context_manager() as session:
            resp = session.execute("SELECT * FROM projects;")
            return tuple([x for x in resp.fetchall()])

    def insert_project(
        self,
        project_name,
        admin_name,
        admin_password
    ):
        with self.session_context_manager() as session:
            project = Project(
                project_name=project_name,
                admin_name=admin_name,
                admin_password=admin_password,
                date_created=date.today()
            )
            session.add(project)
