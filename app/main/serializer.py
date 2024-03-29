from app.auth.serializer import UsersSchema
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

marsh = Marshmallow()

class UsersInfoSchema(marsh.Schema):
    user = fields.Nested(UsersSchema, only=['id', 'user_name', 'full_name'])
    class Meta:
        fields = (
            'user',
            'id',
            'date',
            'info',
            )