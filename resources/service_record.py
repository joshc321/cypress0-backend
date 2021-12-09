#~/cypress/beta1/backend/resources/service_record.py   #completely new file from tempate

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from database.models import ServiceRecord, User, Customer
from flask_restful import Resource, reqparse
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, InternalServerError, ServiceDoesNotExistError, ServiceAlreadyExistsError, BadTokenError
import json
import datetime

class ServicesApi(Resource):
    
    @jwt_required()
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
            #date = datetime.datetime.fromtimestamp(body['date'] / 1000.0)
            if 'date' in body:
                print('body date', body['date'])
                date = datetime.datetime.strptime(body['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                print("Posted date", date)
                body['date'] = date

            if body['address'].strip() == '':
                body['address'] = customer.address
                body['city'] = customer.city
                body['state'] = customer.state
                body['zip'] = customer.zip

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
        parser = reqparse.RequestParser()
        parser.add_argument('id', action='append')
        parsed = parser.parse_args()
        try:
            services = ServiceRecord.objects(id__in=parsed['id']).order_by('-date').to_json()
            return Response(services, mimetype="application/json", status=200)
        except (DoesNotExist, ValidationError):
            raise ServiceDoesNotExistError
        except Exception as e:
            raise InternalServerError