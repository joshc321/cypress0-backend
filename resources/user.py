#~/cypress/beta1/backend/resources/user.py

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, InternalServerError, UserNotFoundError

class UsersApi(Resource):  #previously MoviesApi
    
    @jwt_required()
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)
 
class UserApi(Resource): #previously MovieApi
    @jwt_required()
    def put(self, id):
        try:
            #user_id = get_jwt_identity()
            user = User.objects.get(id=id)
            body = request.get_json()
            user.update(**body)
            user.save()
            user = User.objects.get(id=id).to_json()
            return Response(user, mimetype="application/json", status=200)#'', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UserNotFoundError
        except Exception:
            raise InternalServerError
    
    @jwt_required()
    def delete(self, id):
        try:
            user = User.objects.get(id=id) #, added_by=user_id)
            user.delete()
            return '', 200
        except DoesNotExist:
            raise UserNotFoundError
        except Exception:
            raise InternalServerError
    
    @jwt_required()
    def get(self, id):
        try:
            user = User.objects.get(id=id).to_json()
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotFoundError
        except Exception:
            raise InternalServerError

class ProtectedApi(Resource):
    @jwt_required()
    def get(self):
        try:
            id = get_jwt_identity()
            user = User.objects.get(id=id).to_json()
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotFoundError
        except Exception:
            raise InternalServerError
