from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from config import Config
from .extensions import db, cache
from app.views.common_views import common_ns
from app.views.property_views import property_ns
from app.views.search_views import search_ns


# Create a Flask RESTx API instance
api = Api(
    title='Property Selling Marketplace',
    version='1.0',
    description= 'This API allows for managing real estate properties, including operations like listing, adding, updating, and deleting properties. It is designed for pennyflo Backend assignment.',
)
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)

    # Importing models
    from app import models

    # Import blueprints
    from .views import property_blueprint, search_blueprint, propertyDetails_blueprint

    # Register blueprints
    app.register_blueprint(property_blueprint, url_prefix='/api')
    app.register_blueprint(search_blueprint, url_prefix='/api')
    app.register_blueprint(propertyDetails_blueprint, url_prefix='/api')

    # Initialize API with Flask app
    api.init_app(app)

    # Add the namespace to the API
    api.add_namespace(common_ns, path='/api')
    api.add_namespace(property_ns, path='/api')
    api.add_namespace(search_ns, path='/api')


    return app
