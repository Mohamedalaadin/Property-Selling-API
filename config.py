import os

class Config(object):
	# Database configuration
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# RDS Database Configuration
	RDS_HOSTNAME = os.getenv('RDS_HOSTNAME')
	RDS_PORT = os.getenv('RDS_PORT')
	RDS_DB_NAME = os.getenv('RDS_DB_NAME')
	RDS_USERNAME = os.getenv('RDS_USERNAME')
	RDS_PASSWORD = os.getenv('RDS_PASSWORD')

	SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}"

	# Simple Cache Configuration
	CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')