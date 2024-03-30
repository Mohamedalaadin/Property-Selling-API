from app import db
from app.models import Property
from app import cache

class BuyerService:
    @staticmethod
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def search_properties(filters):
        """
        Searches properties based on various filters.

        :param filters: Dictionary containing filter criteria such as location, number of rooms, and price range.
        :type filters: dict
        :return: List of properties that match the search criteria.
        """
        query = Property.query

        if 'location' in filters:
            query = query.filter(Property.location.ilike(f"%{filters['location']}%"))

        if 'num_rooms' in filters:
            query = query.filter(Property.num_rooms == int(filters['num_rooms']))

        if 'min_price' in filters:
            query = query.filter(Property.price >= float(filters['min_price']))

        if 'max_price' in filters:
            query = query.filter(Property.price <= float(filters['max_price']))

        return query.all()
