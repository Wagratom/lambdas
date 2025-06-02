class jwtException(Exception):
    """Base class for JWT exceptions."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
