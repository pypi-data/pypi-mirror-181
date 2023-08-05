class OperationDBError(Exception):
    def __init__(self, exc, operation: str, code: int = 500, entity=None, **kwargs) -> None:
        self.code = code
        self.exc = exc
        self.entity = entity
        self.operation = operation
        self.extra = kwargs
        self.message = str(exc)
        super().__init__(f"{operation} Error")
