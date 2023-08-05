"""
Define um ou mais validators para categoria
"""

# Python

# Apps
from kernel_catalogo_videos.core.domain.validators import PropsValidated, ValidatorFieldInterface


class DummyValidator(ValidatorFieldInterface[PropsValidated]):
    """
    Validação de serializers do django rest framework
    """

    def validate(self, validator: bool) -> bool:
        if not validator:
            return False

        return True
