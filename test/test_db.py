import pytest


from quesadiya.db.schema import (
    AdminDB,
    Project,
    Collaborator
)
from quesadiya.db.schema import (
    ProjectDB,
    SampleText,
    CandidateGroup,
    TripletDataset
)

import os
from sqlalchemy import create_engine



class TestSchema:

    # ../quesadiya/test
    root_dir = os.path.dirname(os.path.abspath(__file__))

    def test_admindb(self):
        """Test creation of admin.db in sqlalchemy."""
        # create admin db
        db_path = os.path.join(self.root_dir, "test.db")
        db_uri = 'sqlite:///' + db_path
        engine = create_engine(db_uri, echo=True, encoding="utf-8")
        AdminDB.Base.metadata.create_all(engine)
        # check the existence of file
        assert os.path.exists(db_path)
        # check table names in admin.db
        engine = create_engine(db_uri, echo=True, encoding="utf-8")
        expected = set([
            Project.__tablename__,
            Collaborator.__tablename__
        ])
        assert set(engine.table_names()) == expected
        os.remove(db_path)

    def test_projectdb(self):
        """Test creation of project.db in sqlalchemy."""
        # create admin db
        db_path = os.path.join(self.root_dir, "test.db")
        db_uri = 'sqlite:///' + db_path
        engine = create_engine(db_uri, echo=True, encoding="utf-8")
        ProjectDB.Base.metadata.create_all(engine)
        # check the existence of file
        assert os.path.exists(db_path)
        # check table names in admin.db
        engine = create_engine(db_uri, echo=True, encoding="utf-8")
        expected = set([
            SampleText.__tablename__,
            CandidateGroup.__tablename__,
            TripletDataset.__tablename__
        ])
        assert set(engine.table_names()) == expected
        os.remove(db_path)

    def test_create_project(self):
        """Test create command in quesadiya."""
