from functools import wraps
from .errors import AuthenticationError

def authentication_required(func):
    @wraps(func)
    def check_authentication(*args, **kwargs):
        self = args[0]
        if not self.is_authenticated:
            raise AuthenticationError("you must be logged in to perform this action")
        return func(*args, **kwargs)
    return check_authentication
