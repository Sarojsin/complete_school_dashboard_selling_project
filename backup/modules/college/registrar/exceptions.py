# College Registrar Exceptions

class RegistrarError(Exception):
    pass


class RegistrarNotFoundError(RegistrarError):
    pass
