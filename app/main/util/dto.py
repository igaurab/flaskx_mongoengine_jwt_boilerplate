from flask_restx import Namespace, fields


class UserDTO:
    api = Namespace("user", description="user related operations")
    user = api.model(
        "user",
        {
            "email": fields.String(required=True, description="user email address"),
            "username": fields.String(required=True, description="user username"),
            "first_name": fields.String(required=True, description="user first name"),
            "last_name": fields.String(required=True, description="user last name"),
            "password": fields.String(required=True, description="user password"),
            "public_id": fields.String(description="user identifier"),
        },
    )

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
