from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .order.views import order_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter your Bearer Token'
        }
    }

    api = Api(app, 
              title='Pizza Delivery API',
              description='A simple pizza delivery API', 
              authorizations=authorizations,
              security='Bearer Auth'  
            )

    api.add_namespace(order_namespace, path='/order')
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def handle_not_found(error):
        return {'message': 'Not found'}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        return {'message': 'Method not allowed'}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
             'Order': Order
        }

    return app   