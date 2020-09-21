from datetime import date

import warnings

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from .session import SessionContextManager

from .schema import AdminDB, ProjectDB
from .schema import (
    Project,
    ProjectStatusEnum,
    Collaborator,
    TripletDataset,
    TripletStatusEnum,
    SampleText,
    CandidateGroup
)


class SQLAlchemyInterface:
    """Execute sql operations in sqlalchemy."""

    def __init__(self, engine):
        self.engine = engine
        session_maker = sessionmaker(bind=self.engine)
        self.session_context_manager = SessionContextManager(session_maker)

    def get_all_projects(self):
        return self._get_all(Project)

    def get_triplets(self):
        return self._get_all(TripletDataset)

    def get_candidates(self, candidate_group_id):
        with self.session_context_manager(expire_on_commit=True) as session:
            resp = session.execute(
                """select s.sample_body,
                          c.candidate_sample_id
                   from candidate_groups as c
                   left join sample_text as s
                   on c.candidate_sample_id = s.sample_id
                   where c.candidate_group_id = '{}'""".format(candidate_group_id)
            )
            for x in resp:
                yield x

    def get_annotated_triplets(self):
        with self.session_context_manager(expire_on_commit=True) as session:
            resp = session.query(TripletDataset)\
                    .filter(TripletDataset.status == TripletStatusEnum.finished)\
                    .all()
            for x in resp:
                yield x

    def get_annotated_triplets_with_text(self):
        with self.session_context_manager(expire_on_commit=True) as session:
            resp = session.execute(
                """SELECT sa.sample_body AS anchor_sample_text,
                          sp.sample_body AS positive_sample_text,
                          sn.sample_body AS negative_sample_text,
                          t.anchor_sample_id,
                          t.positive_sample_id,
                          t.negative_sample_id
                   FROM triplet_dataset AS t
                   LEFT JOIN sample_text AS sa
                     ON t.anchor_sample_id = sa.sample_id
                   LEFT JOIN sample_text AS sp
                     ON t.positive_sample_id = sp.sample_id
                   LEFT JOIN sample_text AS sn
                     ON t.negative_sample_id = sn.sample_id
                   WHERE t.status = '{}';""".format(TripletStatusEnum.finished.name)
            )
            for x in resp:
                yield x

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

    def is_project_running(self, project_name):
        with self.session_context_manager(expire_on_commit=True) as session:
            result = session.query(Project.status)\
                        .filter(Project.project_name == project_name)\
                        .scalar()
            if result.value == ProjectStatusEnum.running.value:
                return True
            else:
                return False

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
            # delete collabortos assocaited with project first
            project_id = self.get_project_id(project_name)
            session.query(Collaborator)\
                .filter(Collaborator.project_id == project_id)\
                .delete()
            # delete project
            session.query(Project)\
                .filter(Project.project_name == project_name)\
                .delete()

    def get_project(self, project_name):
        with self.session_context_manager(expire_on_commit=False) as session:
            result = session.query(Project)\
                        .filter(Project.project_name == project_name)\
                        .first()
            return result

    def get_project_id(self, project_name):
        with self.session_context_manager(expire_on_commit=True) as session:
            project_id = session.query(Project.project_id)\
                            .filter(Project.project_name == project_name)\
                            .scalar()
            return project_id

    def get_collaborators(self, project_name):
        with self.session_context_manager(expire_on_commit=True) as session:
            project_id = self.get_project_id(project_name)
            resp = session.query(Collaborator)\
                        .join(Project)\
                        .filter(Collaborator.project_id == project_id)\
                        .all()
            for x in resp:
                yield x

    def _update_project(self, field, value, project_name):
        with self.session_context_manager(expire_on_commit=True) as session:
            session.query(Project)\
                .filter(Project.project_name == project_name)\
                .update({field: value})

    def update_project_description(self, project_name, new_description):
        self._update_project(
            field=Project.project_description,
            value=new_description,
            project_name=project_name
        )

    def update_admin_contact(self, project_name, new_contact):
        self._update_project(
            field=Project.admin_contact,
            value=new_contact,
            project_name=project_name
        )

    def change_admin_name(self, project_name, new_admin):
        self._update_project(
            field=Project.admin_name,
            value=new_admin,
            project_name=project_name
        )

    def change_admin_password(self, project_name, new_password):
        self._update_project(
            field=Project.admin_password,
            value=new_password,
            project_name=project_name
        )

    def collaborators_bulk_update(self, collaborators, project_id):
        warned = False
        num_added = 0
        with self.session_context_manager(expire_on_commit=True) as session:
            for x in collaborators:
                result = self._get_or_create(
                    session=session,
                    object_params=x,
                    table=Collaborator,
                    project_id=project_id,
                    collaborator_name=x["collaborator_name"]
                )
                if result[1]:
                    num_added += 1
                if (not result[1]) and (not warned):
                    warnings.warn(
                        "Duplicate collaborator name found during inserting "
                        "new collabortors. Quesadiya skips duplicate "
                        "collaborators in the new file.", RuntimeWarning
                    )
                    warned = True
        return num_added

    def _get_or_create(self, session, object_params, table, **kwargs):
        instance = session.query(table).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            instance = table(**object_params)
            session.add(instance)
            return instance, True

    def triplets_bulk_insert(self, triplets):
        self._bulk_insert(table=TripletDataset, data=triplets)

    def candidate_groups_bulk_insert(self, candidates):
        self._bulk_insert(table=CandidateGroup, data=candidates)

    def sample_text_bulk_insert(self, sample_text):
        self._bulk_insert(table=SampleText, data=sample_text)

    def collaborators_bulk_insert(self, collaboratos):
        self._bulk_insert(table=Collaborator, data=collaboratos)

    def _bulk_insert(self, table, data):
        """Note that this method is implemented in a way recommended in
        sqlalchemy's official documentation.
        (source: https://docs.sqlalchemy.org/en/13/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow).
        """
        self.engine.execute(
            table.__table__.insert(),
            data
        )
