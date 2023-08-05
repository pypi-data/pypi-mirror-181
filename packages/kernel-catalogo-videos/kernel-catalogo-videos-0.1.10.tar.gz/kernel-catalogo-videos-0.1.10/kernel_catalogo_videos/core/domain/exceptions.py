"""
Principais Exceções lançadas pela aplicação
"""
# Apps
from kernel_catalogo_videos.core.domain.validators import ErrorsField


class InvalidUUIDException(Exception):
    """
    Representa um UUID invalido
    """

    def __init__(self, error: str = "Id must be a valid UUID") -> None:
        super().__init__(error)


class ValidationException(Exception):
    """
    Representa erro de validação generico
    """

    pass


class EntityValidationException(Exception):
    """
    Representa uma entidade invalida
    """

    def __init__(self, error: ErrorsField) -> None:
        self.error = error
        super().__init__("Entity Validation Error")


class NotFoundException(Exception):
    """
    Representa uma entidade não encontrada
    """

    pass
