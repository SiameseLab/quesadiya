from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Date,
    Enum,
    DateTime,
    PrimaryKeyConstraint
)

import enum


PARAGRAPH_DELIM = ' <end_of_paragraph> '


# base for admin.db
class AdminDB:
    """Table schema for admin.db."""
    # sqlalchemy base for table
    Base = declarative_base()
    MAX_PROJECT_NAME_CHAR = 30
    MAX_USER_NAME_CHAR = 30
    MAX_PASSWORD_CHAR = 30


# project table schema in admin.db
class Project(AdminDB.Base):
    """Table schema for `projects` table in `admin.db`."""
    __tablename__ = "projects"
    project_id = Column(Integer, index=True, primary_key=True)
    project_name = Column(
        String(AdminDB.MAX_PROJECT_NAME_CHAR),
        index=True,
        nullable=False
    )
    project_description = Column(Text, nullable=True)
    admin_name = Column(String(AdminDB.MAX_USER_NAME_CHAR), nullable=False)
    admin_password = Column(String(AdminDB.MAX_PASSWORD_CHAR), nullable=False)
    date_created = Column(Date, nullable=False)


# collaborator table schema in admin.db
class Collaborator(AdminDB.Base):
    """Table schema for `collaborators` table in `admin.db`."""
    __tablename__ = "collaborators"
    # set foregin key to projects table
    project_id =  Column(
        Integer, ForeignKey("projects.project_id"), nullable=False
    )
    collaborator_name = Column(String(AdminDB.MAX_USER_NAME_CHAR), nullable=False)
    collaborator_password = Column(String(AdminDB.MAX_PASSWORD_CHAR),
                                   nullable=False)
    # set project_id and collaborator_name composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('project_id', 'collaborator_name'),
        {}
    )


# base for project.db
class ProjectDB:
    """Table schema for project db."""
    Base = declarative_base()
    MAX_ID_LEN = 100


# defin enum for sample status column
class DataStatusEnum(enum.Enum):
    unfinished = 0
    finished = 1
    discarded = 2


class SampleText(ProjectDB.Base):
    """Table schema for `sample_text` table in `project.db`."""
    __tablename__ = "sample_text"
    # sample_id is primary key
    sample_id = Column(String(ProjectDB.MAX_ID_LEN), primary_key=True)
    sample_body = Column(Text, nullable=True)
    sample_title = Column(Text, nullable=True)


class CandidateGroup(ProjectDB.Base):
    """Table schema for `candidate_groups` table in `project.db`."""
    __tablename__ = "candidate_groups"
    candidate_group_id = Column(String(ProjectDB.MAX_ID_LEN), nullable=False)
    candidate_sample_id = Column(
        String(ProjectDB.MAX_ID_LEN),
        ForeignKey("sample_text.sample_id"),
        nullable=False
    )
    # set sample_id and candidate_id composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('candidate_group_id', 'candidate_sample_id'),
        {}
    )


class TripletDataset(ProjectDB.Base):
    """Table schema for `triplet_dataset` table in `project.db`."""
    __tablename__ = "triplet_dataset"
    anchor_sample_id = Column(
        String(ProjectDB.MAX_ID_LEN),
        ForeignKey("sample_text.sample_id"),
        nullable=False
    )
    candidate_group_id = Column(
        String(ProjectDB.MAX_ID_LEN),
        ForeignKey("candidate_groups.candidate_group_id"),
        nullable=False
    )
    positive_sample_id = Column(String(ProjectDB.MAX_ID_LEN), nullable=True)
    negative_sample_id = Column(String(ProjectDB.MAX_ID_LEN), nullable=True)
    status = Column(Enum(DataStatusEnum), nullable=False)
    time_changed = Column(DateTime, nullable=False)
    # set anchor_id and candidate_id composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('anchor_sample_id', 'candidate_group_id'),
        {}
    )
