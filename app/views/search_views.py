from flask import Blueprint, request, jsonify
from app.services.buyer_service import BuyerService
from flask_restx import Namespace, Resource, fields, reqparse
from app.models.property import PropertyStatus

bp = Blueprint('search', __name__)

# Define the namespace
search_ns = Namespace(
	'search',
	description='Search for properties by applying filters'
)

property_model = search_ns.model('Property', {
    'id': fields.Integer(required=True, description='The property identifier'),
	'owner_id': fields.Integer(required=True, description='The owner user identifier'),
    'location': fields.String(required=True, description='Location of the property'),
    'num_rooms': fields.Integer(required=True, description='Number of rooms'),
    'price': fields.Float(required=True, description='Price of the property'),
    'status': fields.String(required=True, enum=[e.value for e in PropertyStatus], description='Status of the property')
})

# Parser for the incoming request parameters
search_parser = reqparse.RequestParser()
search_parser.add_argument('location', type=str, help='Location to filter properties')
search_parser.add_argument('num_rooms', type=int, help='Number of rooms to filter properties')
search_parser.add_argument('min_price', type=float, help='Minimum price range for properties')
search_parser.add_argument('max_price', type=float, help='Maximum price range for properties')


@search_ns.route('/properties/search')
class PropertySearch(Resource):
    @search_ns.expect(search_parser)
    @search_ns.marshal_list_with(property_model)
    def get(self):
        """Search for properties based on filters."""
        args = search_parser.parse_args()
        properties = BuyerService.search_properties(args)

        return [property.to_dict() for property in properties]


@bp.route('properties/search', methods=['GET'])
def search_properties_endpoint():
	"""
	Endpoint for searching properties based on filters.
	"""
	# Filters are passed as query parameters, E.g,/search?location=city&min_price=100000
	filters = request.args.to_dict()

	# Convert numeric filters from string to their appropriate types
	if 'num_rooms' in filters:
		filters['num_rooms'] = int(filters['num_rooms'])
	if 'min_price' in filters:
		filters['min_price'] = float(filters['min_price'])
	if 'max_price' in filters:
		filters['max_price'] = float(filters['max_price'])

	properties = BuyerService.search_properties(filters)

	properties_list = [property.to_dict() for property in properties]

	return jsonify(properties=properties_list)