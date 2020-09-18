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
        return self._get_all(Project)

    def get_triplets(self):
        return self._get_all(TripletDataset)

    def _get_all(self, table):
        with self.session_context_manager(expire_on_commit=True) as session:
            resp = session.query(table).all()
            for x in resp:
                yield x

    def insert_project(
        self,
        project_name,
        project_description,
        admin_name,
        admin_password,
        admin_contact,
        status
    ):
        with self.session_context_manager(expire_on_commit=True) as session:
            project = Project(
                project_name=project_name,
                project_description=project_description,
                admin_name=admin_name,
                admin_password=admin_password,
                admin_contact=admin_contact,
                date_created=date.today(),
                status=status
            )
            session.add(project)

    def check_project_exists(self, project_name):
        result = self._check_existence(
            table_field=Project.project_name,
            value=project_name
        )
        return result

    def _check_existence(self, table_field, value):
        with self.session_context_manager(expire_on_commit=True) as session:
            result = session.query(
                exists().where(table_field == value)
            ).scalar()
        return result

    def admin_authentication(self, project_name, admin_name, admin_password):
        with self.session_context_manager(expire_on_commit=True) as session:
            result = session.query(
                exists().
                    where(Project.project_name == project_name).
                    where(Project.admin_name == admin_name).
                    where(Project.admin_password == admin_password)
            ).scalar()
        return result

    def delete_project(self, project_name):
        with self.session_context_manager(expire_on_commit=True) as session:
            session.query(Project).filter(Project.project_name == project_name).delete()

    def get_project(self, project_name):
        with self.session_context_manager(expire_on_commit=False) as session:
            result = session.query(Project).filter(project_name == project_name).first()
            return result

    def get_collaborators(self, project_name):
        with self.session_context_manager(expire_on_commit=True) as session:
            project_id = session.query(Project.project_id).filter(Project.project_name == project_name).scalar()
            resp = session.query(Collaborator).join(Project).filter(Collaborator.project_id == project_id).all()
            for x in resp:
                yield x

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
