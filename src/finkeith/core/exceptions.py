class MissingAPIKeyError(Exception):
    """Exception raised when an API key is missing."""
    def __init__(self, message: str = "API key is missing."):
        self.message = message
        super().__init__(self.message)

class IBankingServiceError(Exception):
    """Base class for all banking service errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)