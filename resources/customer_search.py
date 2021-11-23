#~/cypress/beta1/backend/resources/customer_search.py

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Customer
from flask_restful import Resource, reqparse
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, CustomerAlreadyExistsError, InternalServerError, UpdatingCustomerError, DeletingCustomerError, CustomerNotExistsError
from bson.json_util import dumps

class SearchApi(Resource):  #previously MoviesApi
    
    #@jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=True)
        parsed = parser.parse_args()

        pipeline = [
                { "$match": { "$text" : { "$search" : parsed['q'], "$diacriticSensitive": "true"} }},
                { "$sort": { "score": { "$meta": "textScore" } } }
            ]

        #customers = Customer.objects(address__icontains=parsed['q']).to_json()
        customers = Customer.objects().aggregate(pipeline)
        cust = dumps(list(customers))
        # $text : { $search: <your string> } 
        return Response(cust, mimetype="application/json", status=200)
