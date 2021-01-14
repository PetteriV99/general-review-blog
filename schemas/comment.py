from marshmallow import Schema, fields, post_dump, validate, ValidationError
from schemas.user import UserSchema


def validate_num_of_servings(n):    # doesnt check whether review exists (yet)
    if n == 0:
        raise ValidationError('Review ID must be greater than 0.')


class CommentSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    review_id = fields.Integer(dump_only=True)

    content = fields.String(required=True, validate=[validate.Length(max=512)])
    review_helpful = fields.Boolean(required=False, dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=('email', ))
    is_publish = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data


