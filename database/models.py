#~/cypress/beta1/backend/database/models.py

import datetime

from .db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Document):
    first = db.StringField(required=True, max_length=50)
    last = db.StringField(required=True, max_length=50)
    phone = db.StringField(required=True, max_length=15)
    address = db.StringField(required=True, max_length=120)
    city = db.StringField(required=True, max_length=50)
    state = db.StringField(required=True, max_length=50)
    zip = db.StringField(max_length=20)
    system = db.StringField(max_length=1023)
    notes = db.StringField(max_length=1023)
    serviceRecords = db.ListField(db.ReferenceField('ServiceRecord'), reverse_delete_rule=db.PULL)
    email = db.StringField()
    added_by = db.ReferenceField('User')
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)


class User(db.Document):
    first = db.StringField(required=True, max_length=50)
    last = db.StringField(required=True, max_length=50)
    email = db.EmailField(required=True, unique=True)
    role = db.StringField(max_length=50)
    company = db.StringField(max_length=50)
    password = db.StringField(required=True, min_length=6)
    customers = db.ListField(db.ReferenceField('Customer', reverse_delete_rule=db.PULL))
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)

    def hash_password(self):
        self.password = generate_password_hash(self.password)
    def check_password(self, password):
       return check_password_hash(self.password, password)

#User.register_delete_rule(Movie, 'added_by', db.CASCADE)


class ServiceRecord(db.Document):
    date = db.DateTimeField(required=False)
    address = db.StringField(required=False, max_length=120)
    city = db.StringField(required=False, max_length=50)
    state = db.StringField(required=False, max_length=50)
    zip = db.StringField(max_length=20)
    service = db.StringField(required=False, max_length=1023)
    notes = db.StringField(max_length=1023)
    bill = db.StringField(max_length=20)
    price = db.StringField(max_length=20)
    customer = db.ReferenceField('Customer', required=True)
    added_by = db.ReferenceField('User')
    date = db.DateTimeField(default=datetime.datetime.utcnow)
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)
