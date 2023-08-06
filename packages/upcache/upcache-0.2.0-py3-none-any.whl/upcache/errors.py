class CacheServerConnectionError(IOError):
    """
    Cache server connection error
    """
    def __init__(self) -> None:
        super().__init__("cache server was not available")

class ProtocolError(IOError):
    """
    Cache server protocol error
    """
    def __init__(self, field: str) -> None:
        super().__init__(f"protocol error on '{field}'")
        self.field = field

class InvalidNameError(Exception):
    """
    Cache name error
    """
    def __init__(self, ch: str) -> None:
        super().__init__(f'name contains invalid character "{ch}"')
        self.char = ch

class InvalidNameLengthError(Exception):
    """
    Cache name length error
    """
    def __init__(self) -> None:
        super().__init__(f'name must be between 1-128 characters')


