from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, EmailField


class BlacklistToken(Document):
    token = StringField(unique=True, required=True)
    blacklisted_on = DateTimeField(default=datetime.utcnow)

    def __repr__(self):
        return "<id: token: {}".format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        query = BlacklistToken.objects(token=str(auth_token))
        if query:
            return True
        else:
            return False
