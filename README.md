# Property Selling Marketplace API

This repository contains the backend API for a Property Selling Marketplace, designed to facilitate property transactions between sellers and buyers. The API supports property management operations and enables property search based on various criteria.

## Features

- **Property Management:** Add, remove, update, and read property data.
- **User Management:** Support for different user roles (property_owner, buyer).
- **Property Search:** Search for properties by location, number of rooms, and price range.
- **Role-based Access Control:** (Optional) Only property owners can add/modify properties, while buyers can search for properties.
- **Caching:** (Optional) Implemented caching to improve performance.

## Technologies Used

- Flask for the backend framework.
- SQLAlchemy for ORM.
- Amoazon RDS MySQL as the database.
- heroku cloud platform to deploy the service.
- Swagger for API documentation.


## Setup and Installation

1. Clone the repository:git clone [repository URL]
cd [repository directory]
2. Set up a virtual environment and activate it:python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
3. Install the dependencies: pip install -r requirements.txt
4. Initialize the database: flask db upgrade
5. Run the server: flask run

## Usage

Access the Swagger UI for the API documentation at `[[Swagger URL]](https://property-selling-f3a8e5c1373b.herokuapp.com/)`.

## Additional Information

- **Authorization:** This implementation does not include user authentication and authorization. This is identified as a scope for future development.
- **Extra Endpoints:** Added endpoints to retrieve all users and list properties of a specific user.

## Deployment

The API is deployed on [Heroku/AWS/Azure].

---
This project is part of my application for the Back-end Engineer (Intern) position at PennyFlo Fintech Private Limited.




