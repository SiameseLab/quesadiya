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
    def __call__(self, expire_on_commit):
        """Provide a transactional scope around a series of operations.

        Notes
        -----
        * Default value of `expire_on_commit` is True, so it's preferred unless
          you have any specific reason not to expire session on commit. For
          example, you might want to set it False for get methods. For
          transactional operations (create, delete), it'd be better to set it
          True.
        """
        session = self.session_maker(expire_on_commit=expire_on_commit)
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
