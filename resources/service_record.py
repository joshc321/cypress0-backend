#~/cypress/beta1/backend/resources/service_record.py   #completely new file from tempate

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from database.models import ServiceRecord, User, Customer
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, InternalServerError, ServiceDoesNotExistError, ServiceAlreadyExistsError, BadTokenError

class ServicesApi(Resource):
    
    #@jwt_required()
    def get(self):
        service_records = ServiceRecord.objects().to_json()
        return Response(service_records, mimetype="application/json", status=200)

 
class ServiceApi(Resource):
    
    @jwt_required()
    def post(self, id):  #id -- customer id for the service
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            customer = Customer.objects.get(id=id)
            service = ServiceRecord(**body, customer=customer ,added_by=user)
            service.save()
            customer.update(push__serviceRecords=service)
            customer.save()
            id = service.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise ServiceAlreadyExistsError
        except Exception as e:
            raise InternalServerError
    

    @jwt_required()
    def put(self, id):  #id -- service id
        try:
            #user_id = get_jwt_identity()
            service = ServiceRecord.objects.get(id=id)
            body = request.get_json()
            service.update(**body)
            service.save()
            service = ServiceRecord.objects.get(id=id).to_json()
            return Response(service, mimetype="application/json", status=200)#'', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise ServiceDoesNotExistError
        except Exception:
            raise InternalServerError
    
    @jwt_required()
    def delete(self, id):  #id -- service id
        try:
            #user_id = get_jwt_identity()
            service = ServiceRecord.objects.get(id=id) #, added_by=user_id)
            service.delete()
            return '', 200
        except DoesNotExist:
            raise ServiceDoesNotExistError
        except Exception:
            raise InternalServerError
    
    @jwt_required()
    def get(self, id):  #id -- service id
        try:
            service = ServiceRecord.objects.get(id=id).to_json()
            return Response(service, mimetype="application/json", status=200)
        except (DoesNotExist, ValidationError):
            raise ServiceDoesNotExistError
        except Exception as e:
            raise InternalServerError