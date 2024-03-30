from app import db
from app.models import Property, User
from app.models.user import UserRole
from app.services.buyer_service import BuyerService
from app.services.user_service import UserService
from app import cache

class PropertyOwnerService:

	@staticmethod
	@cache.memoize(timeout=300)
	def view_properties_list(user_id):
		"""
		This function is made for the frontend to fetch a list of properties owned by a specific user.

		:param user_id: The unique identifier for the property owner.
		:type user_id: int

		:return: A list of property objects owned by the user.
		"""
		# Ensure the user has the role of PROPERTY_OWNER
		user = User.query.get(user_id)
		if user is None or user.role != UserRole.PROPERTY_OWNER:
			raise Exception("User not found or not a property owner.")

		# Query the database for properties owned by the user
		properties = Property.query.filter_by(owner_id=user_id).all()

		# Convert the list of Property objects to a list of dictionaries using to_dict()
		properties_list = [property.to_dict() for property in properties]


		return properties_list

	@staticmethod
	def add_property(user_id, property_data):
		"""

		:param user_id: The unique identifier of the user who adding the property.
		:type user_id: int

		:param property_data: A dictionary containing details of the property such as
								location, number of rooms, price, and status.
		:type property_data: dict
		:raises Exception: if the user dose not have permission to add properties.

		The function retrieves the user based on the `user_id`, checks the user's role,
		and creates a new property record in the database with the provided details.
		"""

		# Retrieve the user object based on the provided user ID
		user = User.query.get(user_id)

		# check if the user has the role of PROPERTY_OWNER, if not, raise an exception
		if user.role != UserRole.PROPERTY_OWNER:
			raise Exception("You do not have permission to add properties.")

		# Create a new property instance with the data provided from property_data dictionary
		new_property = Property(
			owner_id=user.id,
			location=property_data['location'],
			num_rooms=property_data['num_rooms'],
			price=property_data['price'],
			status=property_data['status']
		)

		# Add the new property to the database session
		db.session.add(new_property)

		# Commit the session to save the property to the database
		db.session.commit()

		# Invalidate the cache for search_properties
		cache.delete_memoized(BuyerService.search_properties)

		# Invalidate the cache for list_properties
		cache.delete_memoized(PropertyOwnerService.view_properties_list)


	@staticmethod
	def modify_property(user_id, property_id, property_data):
		"""

		:param user_id: The unique identifier of the user who adding the property.
		:type user_id: int

		:param property_id: The id of the property you want to modify.
		:type property_data: int

		:param property_data: A dictionary containing details of the property such as
								location, number of rooms, price, and status.
		:type property_id: dict

		:return: The modified property object after successful update.
		:raises Exception: If the user does not have the PROPERTY_OWNER role, does not own the property,
							or if the specified property cannot be found.

		The function updates the property's location, number of rooms, price, and status as per the provided
		data. It then commits these changes to the database.
		"""

		# Retrieve the user object based on the provided user ID
		user = User.query.get(user_id)

		# check if the user has the role of PROPERTY_OWNER, if not, raise an exception
		if user.role != UserRole.PROPERTY_OWNER:
			raise Exception("You do not have permission to update properties.")

		# Fetch the property to be modified from the database using the property ID
		property_to_modify = Property.query.get(property_id)

		# Check if the property exist and belong to the owner

		if property_to_modify is None:
			raise Exception("Property not found.")
		if property_to_modify.owner_id != int(user_id):
			raise Exception(f"You do not own this property.")

		# Modify the property details with new data provided
		property_to_modify.location = property_data.get('location', property_to_modify.location)
		property_to_modify.num_rooms = property_data.get('num_rooms', property_to_modify.num_rooms)
		property_to_modify.price = property_data.get('price', property_to_modify.price)
		property_to_modify.status = property_data.get('status', property_to_modify.status)

		# Commit the changes to the database
		db.session.commit()

		# Invalidate the cache for search_properties
		cache.delete_memoized(BuyerService.search_properties)
		# Invalidate the cache for this specific property in view_property
		cache.delete_memoized(UserService.view_property, property_id)
		# Invalidate the cache for list_properties
		cache.delete_memoized(PropertyOwnerService.view_properties_list)

		return property_to_modify

	@staticmethod
	def delete_property(user_id, property_id):
		"""
		Deletes a property from the database.

		:param user_id: The unique identifier of the user attempting to delete the property. Must be the property owner.
		:type user_id: int
		:param property_id: The ID of the property to be deleted.
		:type property_id: int
		:raises Exception: If the property cannot be found, if the user does not have permission to delete the property, or if the user is not the owner of the property.
		"""
		# Retrieve the user object based on the provided user ID
		user = User.query.get(user_id)

		# Check if the user has the role of PROPERTY_OWNER, if not, raise an exception
		if user.role != UserRole.PROPERTY_OWNER:
			raise Exception("You do not have permission to delete properties.")

		# Fetch the property to be deleted from the database using the property ID
		property_to_delete = Property.query.get(property_id)

		# Check if the property exists and belongs to the owner
		if property_to_delete is None:
			raise Exception("Property not found.")
		if property_to_delete.owner_id != int(user_id):
			raise Exception("You do not own this property.")

		# Delete the property from the database
		db.session.delete(property_to_delete)
		db.session.commit()

		# Invalidate the cache for search_properties
		cache.delete_memoized(BuyerService.search_properties)
		# Invalidate the cache for this specific property in view_property
		cache.delete_memoized(UserService.view_property, property_id)
		# Invalidate the cache for list_properties
		cache.delete_memoized(PropertyOwnerService.view_properties_list)

