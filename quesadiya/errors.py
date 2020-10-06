class QuesadiyaCommandError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class AuthenticationError(Exception):
    def __init__(self, project_name):
        msg = "Invalid name or password for project '{}'.".format(project_name)
        super().__init__(msg)


class ProjectNotExistError(RuntimeError):
    def __init__(self, project_name):
        msg = ("Project '{}' doesn't exist. Check all project names by "
               "`quesadiya inspect all`.".format(project_name))
        super().__init__(msg)


class ProjectRunningError(RuntimeError):
    def __init__(self, project_name, operation):
        msg = ("Project '{}' is currently running. Try {} when the project "
               "is not running.".format(project_name, operation))
        super().__init__(msg)


class ProjectExistsError(RuntimeError):
    def __init__(self, project_name):
        msg = ("Project '{}' already exists.".format(project_name))
        super().__init__(msg)


class NotJSONLFileError(ValueError):
    def __init__(self, argument, path):
        msg = ("The extension of {} input must be jsonl (jsonlines file), "
               "instead received: {}.".format(argument, path))
        super().__init__(msg)
