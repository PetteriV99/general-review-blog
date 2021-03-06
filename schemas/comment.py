from marshmallow import Schema, fields, post_dump, validate, ValidationError
from schemas.user import UserSchema


def validate_bool(n):
    if type(n) != bool:
        raise ValidationError('Review helpful must be bool (true or false)')


class CommentSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    review_id = fields.Integer(dump_only=True)
    content = fields.String(required=True, validate=[validate.Length(max=512)])
    review_helpful = fields.Boolean(required=True, validate=validate_bool)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=('email', ))
    is_publish = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data


