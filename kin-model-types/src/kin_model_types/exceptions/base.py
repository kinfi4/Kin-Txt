class EntityNotFoundException(Exception):
    pass


class UserModelNotFoundException(EntityNotFoundException):
    pass


class UserTemplateNotFoundException(EntityNotFoundException):
    pass


class ImpossibleToUpdateCustomModelException(Exception):
    pass


class ImpossibleToDeleteCustomModelException(Exception):
    pass


class ModelAlreadyExistsException(Exception):
    pass
