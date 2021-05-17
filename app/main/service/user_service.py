import uuid
import datetime
from app.main.model.user import User
from loguru import logger
from app.main import flask_bcrypt

class ResponseObject:
    @staticmethod
    def user_reg(success=False):
        if success:
            message = {"status": "success", "message": "User registration successful!"}
            return message, 201
        else:
            message = {"status": "fail", "message": "User already exists!"}
            return message, 400


def save_new_user(data):
    user = User.objects(email=data["email"])
    if not user:
        hashed_password = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=hashed_password
        )
        new_user.save()
        logger.debug("NEW USER CREATED: ", new_user)
        return generate_token(new_user)
    else:
        return ResponseObject.user_reg(success=False)


def get_user(public_id):
    query_set = User.objects(public_id=public_id)
    if query_set:
        user = query_set[0]
        del user.password
        return user
    else:
        return None

def generate_token(user):
    logger.info(f"Generate Token User: {user.id}")
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        logger.info(f"Auth Token: {type(auth_token)}")
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        logger.error(f"Generate Token Error {e}")
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401