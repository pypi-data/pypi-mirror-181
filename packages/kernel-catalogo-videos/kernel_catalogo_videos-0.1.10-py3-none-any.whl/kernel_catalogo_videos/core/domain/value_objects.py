"""
Como exemplo de Value Objects podemos citar objetos que representam
Nome, Endereco, Email, Dinheiro, etc.

Um objeto Dinheiro com valor R$ 5,00 é igual a outro objeto de mesmo valor;
um objeto Nome com valor 'Jose' é igual a outro objeto de mesmo valor não
importando a instância do objeto.

Os Value Objects devem ser imutáveis e pequenos e
representam algo único como quantidades, descrições simples, valores,

Ser imutável
Seu único uso é como propriedade de uma ou mais entidades ou mesmo outro VO;
Saber usar todas as suas propriedades ao realizar qualquer tipo de
verificação de igualdade, incluindo aquelas que
baseiam sua comparação em códigos hash;

Sua lógica não deve ter efeitos colaterais no estado fora do VO;

"""

# Python
import json
from abc import ABC
from dataclasses import fields, dataclass


@dataclass(frozen=True)
class ValueObject(ABC):
    """
    Representa o  str de uma entidade
    """

    def __str__(self) -> str:
        fields_names = [field.name for field in fields(self)]
        return (
            str(getattr(self, fields_names[0]))
            if len(fields_names) == 1
            else json.dumps({field_name: getattr(self, field_name) for field_name in fields_names})
        )
