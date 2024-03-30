from flask import Blueprint, jsonify
from app.services.user_service import UserService
from flask_restx import Namespace, fields, Resource
from app.models.user import UserRole

# Define the blueprint
bp = Blueprint('common', __name__)

# Define the namespace
common_ns = Namespace('common operations', description='Common operations')

# Define the model for your Swagger documentation (if needed)
user_model = common_ns.model('User', {
    'id': fields.Integer(required=True, description='The user unique identifier'),
    'name': fields.String(required=True, description="The user's name"),
    'email': fields.String(required=True, description="The user's email address", unique=True),
    'mobile': fields.String(description="The user's mobile number"),
    'role': fields.String(required=True, enum=[role.value for role in UserRole], description="The user's role"),
})

@common_ns.route('/users')
class UserList(Resource):
    @common_ns.doc('list_users')
    @common_ns.marshal_list_with(user_model)
    def get(self):
        """Fetch all users"""
        return UserService.get_all_users()
