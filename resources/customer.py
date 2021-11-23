#~/cypress/beta1/backend/resources/customer.py     #previously movie.py

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Customer, User
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, CustomerAlreadyExistsError, InternalServerError, UpdatingCustomerError, DeletingCustomerError, CustomerNotExistsError

class CustomersApi(Resource):  #previously MoviesApi
    
    #@jwt_required()
    def get(self):
        customers = Customer.objects().to_json()
        return Response(customers, mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            customer = Customer(**body, added_by=user)
            customer.save()
            user.update(push__customers=customer)
            user.save()
            id = customer.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise CustomerAlreadyExistsError
        except Exception as e:
            raise InternalServerError
 
class CustomerApi(Resource): #previously MovieApi
    @jwt_required()
    def put(self, id):
        try:
            #user_id = get_jwt_identity()
            customer = Customer.objects.get(id=id)
            body = request.get_json()
            customer.update(**body)
            customer.save()
            customer = Customer.objects.get(id=id).to_json()
            return Response(customer, mimetype="application/json", status=200)#'', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingCustomerError
        except Exception:
            raise InternalServerError
    
    @jwt_required()
    def delete(self, id):
        try:
            #user_id = get_jwt_identity()
            customer = Customer.objects.get(id=id) #, added_by=user_id)
            customer.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingCustomerError
        except Exception:
            raise InternalServerError
    
    @jwt_required()
    def get(self, id):
        try:
            customer = Customer.objects.get(id=id).to_json()
            return Response(customer, mimetype="application/json", status=200)
        except DoesNotExist:
            raise CustomerNotExistsError
        except Exception:
            raise InternalServerError
