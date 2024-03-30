from app import db
from app.models import Property, User
from app.models.user import UserRole
from app import cache

class UserService:
	@staticmethod
	def get_all_users():
		"""
		This function is for the frontend, gets all users so you can choose between users to test without a authorization
		:return: List of users
		"""
		try:
			users = User.query.all()
			users_list = [
				{'id': user.id, 'name': user.name, 'email': user.email, 'mobile': user.mobile, 'role': user.role.name if user.role else None}
				for user in users
			]
			return users_list
		except Exception as e:
			raise Exception(f"Failed to fetch users: {e}")
	@staticmethod
	@cache.memoize(timeout=300)
	def view_property(property_id):
		"""
		Retrieves details for a specific property.

		:param property_id: The ID of the property to view.
		:type property_id: int

		:return: A dictionary with property details or None if not found.
		:rtype: dict
		"""
		property = Property.query.get(property_id)
		if property:
			return {
				"id": property.id,
				"owner_id": property.owner_id,
				"location": property.location,
				"num_rooms": property.num_rooms,
				"price": property.price,
				"status": property.status.value
			}
		else:
			raise Exception("Property not found.")