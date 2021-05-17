import uuid
from datetime import datetime
from datetime import timedelta
from mongoengine import Document, StringField, DateTimeField, EmailField
from app.main import flask_bcrypt
import jwt
from app.main.model.blacklist import BlacklistToken
from app.main.config import key
from loguru import logger

class User(Document):
    email = EmailField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    registered_on = DateTimeField(default=datetime.utcnow)
    public_id = StringField(required=True, unique=True,
                            default=str(uuid.uuid4()))

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
            Generates the Auth Token
            :return: string
            """
        logger.debug(f"user_id: {user_id}" )
        user_id = str(user_id)
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            logger.debug(f"Payload: {payload}")
            auth_code =  jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )

            return auth_code
        except Exception as e:
            logger.error(f"Encode Auth Token: {e}")
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
        """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
        """
        logger.info(f"Decode Auth Token: {auth_token}")
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        logger.info(f"is_blacklisted: {is_blacklisted_token}")
        if is_blacklisted_token:
            return {'error':'Token blacklisted. Please log in again.'}
        else:
            try:
                payload = jwt.decode(auth_token, key, algorithms='HS256')
                return payload['sub']
            except jwt.ExpiredSignatureError:
                return {'error': 'Signature expired. Please log in again.'}
            except jwt.InvalidTokenError:
                return {'error':'Invalid token. Please log in again.'}
