from marshmallow import Schema, fields, post_dump, validate, ValidationError

from schemas.user import UserSchema


def validate_rating(n):
    if n < 1:
        raise ValidationError('Rating must be greater than 0.')
    if n > 10:
        raise ValidationError('Rating must not be greater than 10.')


class ReviewSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)

    title = fields.String(required=True, validate=[validate.Length(max=256)])
    content = fields.String(validate=[validate.Length(max=1024)])
    rating = fields.Integer(validate=validate_rating)

    is_publish = fields.Boolean(dump_only=True)
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=('email', ))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data
