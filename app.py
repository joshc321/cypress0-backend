#~/cypress/beta1/backend/app.py

from flask import Flask
from flask_jwt_extended import JWTManager
from database.db import initialize_db
from flask_restful import Api
from resources.errors import errors
from flask_mail import Mail


app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
#app.config['PROPAGATE_EXCEPTIONS'] = True
mail = Mail(app)

# imports requiring app and mail
from resources.routes import initialize_routes

api = Api(app, errors=errors)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)

