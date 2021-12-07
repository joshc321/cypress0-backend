from resources.errors import UnauthorizedError, InternalServerError
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
import flask_restful

def error_handler() -> object:
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            # handle different types of errors and return messages accordingly with status code
            except Exception as e:
                if isinstance(e, ExpiredSignatureError):
                    raise UnauthorizedError
                else:
                    raise UnauthorizedError
        return wrapped
    return wrapper

class Resource(flask_restful.Resource):
    method_decorators = [error_handler]   # applies to all inherited resources