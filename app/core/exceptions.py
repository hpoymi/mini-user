class ApplicationError(Exception):
    pass


class UserNotFoundError(ApplicationError):
    pass


class ProjectNotFoundError(ApplicationError):
    pass


class EmailAlreadyExistsError(ApplicationError):
    pass
