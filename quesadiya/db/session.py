from contextlib import contextmanager


class SessionContextManager:
    """Creates a session context object when being called. It commits changes
    made in a session when code exits without any exception. If it receives
    some exception, it rollbacks changes. At the end, it closes session. This
    way is recommended in sqlalchemy's official documentation.

    Source
    ------
        https://docs.sqlalchemy.org/en/13/orm/session_basics.html
    """

    def __init__(self, session_maker):
        self.session_maker = session_maker

    @contextmanager
    def __call__(self):
        """Provide a transactional scope around a series of operations."""
        session = self.session_maker()
        try:
            # enforce foreign key constraints
            session.execute("PRAGMA foreign_keys = ON;")
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
