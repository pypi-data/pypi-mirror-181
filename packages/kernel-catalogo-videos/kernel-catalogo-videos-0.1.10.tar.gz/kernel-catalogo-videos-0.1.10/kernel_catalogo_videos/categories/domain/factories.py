"""
Define factories para o dominio Category
"""


class CategoryValidatorFactory:
    """
    Representa uma factory pattern para criar um validator
    """

    @staticmethod
    def create(serializer_class):
        """
        Instancia uma classe do tipo Validator
        """
        return serializer_class()
