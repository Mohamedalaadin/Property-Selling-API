from flask import request ,Blueprint, jsonify
from app import db
from app.models.property import Property, PropertyStatus
from app.services.property_owner_service import PropertyOwnerService
from app.services.user_service import UserService
from flask_restx import Namespace, Resource, fields, reqparse, abort

bp = Blueprint('property', __name__)
# Define the namespace
property_ns = Namespace(
	'properties',
	description='operations related to properties E.G, list, view, add, modify and delete properties'
)

# Define models for Swagger documentation
property_model = property_ns.model('Property', {
    'id': fields.Integer(required=True, description='The property identifier'),
	'owner_id': fields.Integer(required=True, description='The owner user identifier'),
    'location': fields.String(required=True, description='Location of the property'),
    'num_rooms': fields.Integer(required=True, description='Number of rooms'),
    'price': fields.Float(required=True, description='Price of the property'),
    'status': fields.String(required=True, enum=[e.value for e in PropertyStatus], description='Status of the property')
})
property_creation_model = property_ns.model('PropertyCreation', {
    'location': fields.String(required=True, description='Location of the property'),
    'num_rooms': fields.Integer(required=True, description='Number of rooms'),
    'price': fields.Float(required=True, description='Price of the property'),
    'status': fields.String(required=True, enum=[status.value for status in PropertyStatus],
                            description='Status of the property')
})
property_modify_model = property_ns.model('PropertyModifaction', {
    'location': fields.String(required=False, description='Location of the property'),
    'num_rooms': fields.Integer(required=False, description='Number of rooms'),
    'price': fields.Float(required=False, description='Price of the property'),
    'status': fields.String(required=False, enum=[status.value for status in PropertyStatus],
                            description='Status of the property')
})

# Define parsers for input data
property_parser = reqparse.RequestParser()
property_parser.add_argument('X-User-Id', location='headers', required=True, help='User ID')

@property_ns.route('/')
class PropertyList(Resource):
    @property_ns.expect(property_parser)
    @property_ns.marshal_list_with(property_model, envelope='properties')
    def get(self):
        """List all properties related to a user"""
        args = property_parser.parse_args()
        user_id = args['X-User-Id']
        try:
            properties = PropertyOwnerService.view_properties_list(user_id)
            return properties
        except Exception as e:
	        if "do not have permission" in str(e):
	            abort(403, str(e))
	        else:
	            abort(400, str(e))

    @property_ns.expect(property_parser, property_creation_model, validate=True)
    @property_ns.response(201, 'Property successfully added')
    @property_ns.response(400, 'Validation Error')
    def post(self):
        """Create a new property"""
        args = property_parser.parse_args()
        user_id = args['X-User-Id']
        property_data = request.json
        try:
	        # Attempt to add the property
	        PropertyOwnerService.add_property(user_id, property_data)
	        return {'message': 'Property added successfully'}, 201
        except Exception as e:
	        if "do not have permission" in str(e):
		        abort(403, str(e))
	        else:
		        abort(400, str(e))

@property_ns.route('/<int:id>')
class PropertyOperations(Resource):
    @property_ns.doc('get_property')
    @property_ns.response(404, 'Property not found')
    @property_ns.marshal_with(property_model)
    def get(self, id):
        """Fetch a single property by its ID"""
        property = UserService.view_property(id)
        if property:
            return property
        property_ns.abort(404, "Property not found")

    @property_ns.expect(property_modify_model, property_parser , validate=True)
    @property_ns.response(204, 'Property successfully updated')
    def put(self, id):
        """Update a property related to a user by its ID"""
        args = property_parser.parse_args()
        user_id = args['X-User-Id']

        property_data = request.json
        updated_property = PropertyOwnerService.modify_property(user_id, id, property_data)
        return {
	               'message': f'Property {id} updated successfully',
	               'property': updated_property.to_dict()
               }, 200

    @property_ns.expect(property_parser, validate=True)
    @property_ns.response(204, 'Property successfully deleted')
    def delete(self, id):
        """Delete a property with ID"""
        args = property_parser.parse_args()
        user_id = args['X-User-Id']

        PropertyOwnerService.delete_property(user_id, id)
        return {'message': f'Property {id} deleted successfully'}, 200

@bp.route('/properties', methods=['GET'])
def get_properties_list_endpoint():

	user_id = request.headers.get("X-User-Id")

	try:
		properties = PropertyOwnerService.view_properties_list(user_id)
		properties_list = [property.to_dict() for property in properties]
		return jsonify(properties= properties_list), 200
	except PermissionError as e:
		# Permission denied error handling
		return jsonify(message=str(e)), 403
	except Exception as e:
		print(f"Error: {e}")  # Or use logging.error(f"Error: {e}")
		return jsonify(message=str(e)), 500

@bp.route('/properties', methods=['POST'])
def add_property_endpoint():
	"""
	Endpoint to create a new property entry in the database.
	Note: As authorization was not part of the assignment requirements, the user ID is passed via the 'X-User-Id' header.

	:return: A JSON response with a success or error message.
	:rtype: flask.Response
	"""
	property_data = request.json
	user_id = request.headers.get("X-User-Id")

	try:
		# Pass the user_id and property_data to function add_property at the service layer
		PropertyOwnerService.add_property(user_id, property_data)
		return jsonify(message="Property added successfully"), 201
	except PermissionError as e:
		# Permission denied error handling
		return jsonify(message=str(e)), 403
	except Exception as e:
		print(f"Error: {e}")  # Or use logging.error(f"Error: {e}")
		return jsonify(message=str(e)), 500


@bp.route('/properties/<int:id>', methods=['PUT'])
def modify_property_endpoint(id):

	"""
	Endpoint to modify an existing property. Expects property data in the request JSON and the user ID in the request headers.
	Note: As authorization was not part of the assignment requirements, the user ID is passed via the 'X-User-Id' header.

	:param id: The ID of the property to modify. Must be the property owner.
	:type id: int

	:return: A JSON response with success or error message.
	:rtype: flask.Response
	"""
	property_data = request.json
	user_id = request.headers.get("X-User-Id")

	try:
		# Pass the user_id ,id and property_data to function modify_property at the service layer
		updated_property = PropertyOwnerService.modify_property(user_id, id, property_data)
		return jsonify(message=f"Property {updated_property.id} updated successfully"), 200
	except Exception as e:
		# Log the actual error message to your console or log file
		print(f"Error: {e}")  # Or use logging.error(f"Error: {e}")
		return jsonify(message=str(e)), 500

@bp.route('/properties/<int:id>', methods=['DELETE'])
def delete_property_endpoint(id):
	"""
	Endpoint to delete an existing property. Requires the user ID to be provided in the request headers.

	:param id: The ID of the property to delete.
	:type id: int

	:return: A JSON response with success or error message.
	:rtype: flask.Response
	"""

	user_id = request.headers.get("X-User-Id")

	try:
		PropertyOwnerService.delete_property(user_id, id)
		return jsonify(message=f"Property {id} deleted successfully"), 200
	except Exception as e:
		print(f"Error: {e}")
		return jsonify(message=str(e)), 500
