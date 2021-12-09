#~/cypress/beta1/backend/resources/errors.py

class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class CustomerAlreadyExistsError(Exception):
    pass

class UpdatingCustomerError(Exception):
    pass

class DeletingCustomerError(Exception):
    pass

class CustomerNotExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class EmailDoesnotExistsError(Exception):
    pass

class BadTokenError(Exception):
    pass

class ExpiredTokenError(Exception):
    pass

class ServiceDoesNotExistError(Exception):
    pass

class ServiceAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "CustomerAlreadyExistsError": {
         "message": "Customer already exists",
         "status": 400
     },
     "UpdatingCustomerError": {
         "message": "Customer not found",
         "status": 404
     },
     "DeletingCustomerError": {
         "message": "Customer not found, could not delete",
         "status": 404
     },
     "CustomerNotExistsError": {
         "message": "Customer with given id doesn't exists",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "Email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },
     "EmailDoesnotExistsError": {
         "message": "Couldn't find the user with given email address",
         "status": 400
     },
     "BadTokenError": {
         "message": "Invalid token",
         "status": 403
      },
      "ExpiredTokenError":{
          "message": "Expired token",
          "status": 403
      },
      "ServiceDoesNotExistError":{
          "message": "Service record not found",
          "status": 404
      },
      "ServiceAlreadyExistsError":{
          "message": "Service record already exist",
          "status": 400
      },
      "NoAuthorizationError":{
          "message": "Missing Authorization Header",
          "status": 400
      },
      "UserNotFoundError":{
          "message": "User not found",
          "status": 400
      },
      "ExpiredSignatureError":{
          "message": "Expired Token",
          "status": 403
      },
      "InvalidTokenError":{
          "message": "Invalid Token",
          "status": 403
      },
      "DecodeError":{
          "message": "No auth",
          "status": 403
      }
}