from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    PrimaryKeyConstraint
)


class AdminDB:
    """Table schema for admin.db."""
    # sqlalchemy base for table
    Base = declarative_base()
    MAX_PROJECT_NAME_CHAR = 30
    MAX_USER_NAME_CHAR = 30
    MAX_PASSWORD_CHAR = 30

# table schemas for admin.db
class Projects(AdminDB.Base):
    """Table schema for `projects` table in `admin.db`."""
    __tablename__ = "projects"
    project_id = Column(Integer, index=True, primary_key=True)
    project_name = Column(String(AdminDB.MAX_PROJECT_NAME_CHAR), nullable=False)
    owner_name = Column(String(AdminDB.MAX_USER_NAME_CHAR), nullable=False)
    owner_password = Column(String(AdminDB.MAX_PASSWORD_CHAR), nullable=False)
    date_created = Column(Date(), nullable=False)

class Collaborators(AdminDB.Base):
    """Table schema for `collaborators` table in `admin.db`."""
    __tablename__ = "collaborators"
    # set foregin key to projects table
    project_id =  Column(
        Integer, ForeignKey("projects.project_id"), nullable=False
    )
    collaborator_name = Column(String(AdminDB.MAX_USER_NAME_CHAR), nullable=False)
    collaborator_password = Column(String(AdminDB.MAX_PASSWORD_CHAR),
                                   nullable=False)
    # set project_id and collaborator_name primary key
    __table_args__ = (
        PrimaryKeyConstraint('project_id', 'collaborator_name'),
        {}
    )


class ProjectDB:
    """Table schema for project db."""
    Base = declarative_base()
    MAX_PROJECT_NAME_CHAR = 30
    MAX_USER_NAME_CHAR = 30
    MAX_PASSWORD_CHAR = 30


class Data(ProjectDB.Base):
    """Table schema for `projects` table in `admin.db`."""
    __tablename__ = "data"
    project_id = Column(Integer, index=True, primary_key=True)
    project_name = Column(String(AdminDB.MAX_PROJECT_NAME_CHAR), nullable=False)
    owner_name = Column(String(AdminDB.MAX_USER_NAME_CHAR), nullable=False)
    owner_password = Column(String(AdminDB.MAX_PASSWORD_CHAR), nullable=False)
    date_created = Column(Date(), nullable=False)
