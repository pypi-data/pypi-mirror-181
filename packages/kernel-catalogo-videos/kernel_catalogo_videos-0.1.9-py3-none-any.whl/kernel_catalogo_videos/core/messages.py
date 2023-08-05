# Python
from enum import Enum


class Messages(Enum):
    FIELD_REQUIRED = "Campo obrigatório."
    INVALID_DATA = "Ocorreu um erro nos campos informados."
    DOES_NOT_EXIST = "Este(a) {} não existe."
    EXCEPTION = "Ocorreu um erro no servidor. Contate o administrador."
    ALREADY_EXISTS = "Já existe um(a) {} com estes dados."
    NO_DATA = "Nenhum dado foi postado."
    PASSWORD_DIDNT_MATCH = "As senhas não conferem."  # nosec
    PASSWORD_CHANGED_OK = "A senha foi alterada com sucesso."  # nosec
    USER_INACTIVE = "Este usuário está inativo."
    USER_HAS_NO_PERMISSIONS = "Este usuário não possui permissões necessárias."

    RESOURCE_CREATED = "{} criado(a)."
    RESOURCE_FETCHED_PAGINATED = "Lista os/as {} paginados(as)."
    RESOURCE_FETCHED = "{} retornado(a)."
    RESOURCE_UPDATED = "{} atualizado(a)."
    RESOURCE_DELETED = "{} deletado(a)."

    TOKEN_CREATED = "Token criado."  # nosec
    INVALID_CREDENTIALS = "As credenciais estão inválidas para log in."  # nosec
    TOKEN_EXPIRED = "Token expirou."  # nosec
    PERMISSION_DENIED = "Permissão negada."

    RESOURCE_NOT_ALLOWED = "O método solicitado não é permitido para este endpoint."
    RESOURCE_NOT_FOUND = "Recurso não encontrado."
    RESOURCE_BAD_REQUEST = "Houve um erro na requisição."
    RESOURCE_DOES_NOT_EXIST = "Um recurso com este ID não existe mais."
    RESOURCE_USER_ALREADY_EXISTS = "Um usuário com este username já existe."

    PARAM_IS_STRING = "O parâmetro {} precisa ser um string"
    PARAM_IS_DICT = "O parâmetro {} precisa ser um dict"
    PARAM_IS_INT = "O parâmetro {} precisa ser um int"
