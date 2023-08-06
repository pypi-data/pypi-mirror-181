class EDnevnikException(Exception):
    """Base e-Dnevnik exception."""
    pass

class AuthenticationError(EDnevnikException):
    """Authentication error."""
    pass
