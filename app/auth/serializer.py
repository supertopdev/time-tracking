from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

marsh = Marshmallow()

class UsersSchema(marsh.Schema):
    class Meta:
        fields = (
            'id',
            'username',
            'full_name',
            'email',
            'email_reminder',
            'role',
            )
