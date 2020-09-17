from datetime import date

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from .session import SessionContextManager

from .schema import AdminDB, ProjectDB
from .schema import (
    Project,
    Collaborator,
    TripletDataset,
    SampleText,
    CandidateGroup
)


class SQLAlchemyInterface:
    """Execute sql operations in sqlalchemy.

    Notes
    -----
    * bulk insert methods are implemented in a way recommended by sqlalchemy's
      official documentation (source: https://docs.sqlalchemy.org/en/13/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow).
    """

    def __init__(self, engine):
        self.engine = engine
        session_maker = sessionmaker(bind=self.engine)
        self.session_context_manager = SessionContextManager(session_maker)

    def get_all_projects(self):
        with self.session_context_manager() as session:
            resp = session.execute("SELECT * FROM projects;")
            return tuple([x for x in resp.fetchall()])

    def insert_project(
        self,
        project_name,
        project_description,
        admin_name,
        admin_password,
        admin_contact
    ):
        with self.session_context_manager() as session:
            project = Project(
                project_name=project_name,
                project_description=project_description,
                admin_name=admin_name,
                admin_password=admin_password,
                admin_contact=admin_contact,
                date_created=date.today()
            )
            session.add(project)

    def get_triplets(self):
        with self.session_context_manager() as session:
            resp = session.execute("SELECT * FROM triplet_dataset;")
            return tuple([x for x in resp.fetchall()])

    def check_project_exists(self, project_name):
        result = self._check_existence(
            table_field=Project.project_name,
            value=project_name
        )
        return result

    def _check_existence(self, table_field, value):
        with self.session_context_manager() as session:
            result = session.query(
                exists().where(table_field == value)
            ).scalar()
        return result

    def admin_authentication(self, project_name, admin_name, admin_password):
        with self.session_context_manager() as session:
            result = session.query(
                exists().
                    where(Project.project_name == project_name).
                    where(Project.admin_name == admin_name).
                    where(Project.admin_password == admin_password)
            ).scalar()
        return result

    def delete_project(self, project_name):
        with self.session_context_manager() as session:
            session.query(Project).filter(Project.project_name==project_name).delete()

    def get_project(self, project_name):
        with self.session_context_manager() as session:
            result = session.query(Project).filter_by(project_name=project_name)
        return list(result)[0]

    def triplets_bulk_insert(self, triplets):
        self.engine.execute(
            TripletDataset.__table__.insert(),
            triplets
        )

    def candidate_groups_bulk_insert(self, candidates):
        self.engine.execute(
            CandidateGroup.__table__.insert(),
            candidates
        )

    def sample_text_bulk_insert(self, sample_text):
        self.engine.execute(
            SampleText.__table__.insert(),
            sample_text
        )
