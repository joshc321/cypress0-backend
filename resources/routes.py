#~/cypress/beta1/backend/resources/routes.py

from .customer import CustomersApi, CustomerApi
from .auth import NewUserApi, LoginApi, Authorized
from .reset_password import ForgotPassword, ResetPassword
from .service_record import ServicesApi, ServiceApi
from .user import UsersApi, UserApi, ProtectedApi
from .customer_search import SearchApi

def initialize_routes(api):
    api.add_resource(CustomersApi, '/api/customers')
    api.add_resource(CustomerApi, '/api/customers/<id>')
    api.add_resource(SearchApi, '/api/customers/search')
    api.add_resource(NewUserApi, '/api/auth/newuser')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(Authorized, '/api/auth/authorized')
    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/api/auth/reset')
    api.add_resource(ServicesApi, '/api/services')
    api.add_resource(ServiceApi, '/api/services/<id>')
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<id>')
    api.add_resource(ProtectedApi, '/api/protected')
    