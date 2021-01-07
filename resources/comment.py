import os

from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.comment import Comment
from schemas.comment import CommentSchema

comment_schema = CommentSchema()
comment_list_schema = CommentSchema(many=True)


class CommentListResource(Resource):

    def get(self):

        comments = Comment.get_all_published()

        return comment_list_schema.dump(comments).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = comment_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        comment = Comment(**data)
        comment.user_id = current_user
        comment.save()

        return comment_schema.dump(comment).data, HTTPStatus.CREATED


class CommentResource(Resource):

    @jwt_optional
    def get(self, comment_id):

        comment = Comment.get_by_id(comment_id=comment_id)

        if comment is None:
            return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if comment.is_publish == False and comment.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return comment_schema.dump(comment).data, HTTPStatus.OK

    @jwt_required
    def patch(self, comment_id):

        json_data = request.get_json()

        data, errors = comment_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        comment = Comment.get_by_id(comment_id=comment_id)

        if comment is None:
            return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != comment.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        comment.content = data.get('content') or comment.content
        comment.nickname = data.get('nickname') or comment.nickname
        comment.review_id = data.get('review_id') or comment.review_id

        comment.save()

        return comment_schema.dump(comment).data, HTTPStatus.OK

    @jwt_required
    def delete(self, comment_id):

        comment = Comment.get_by_id(comment_id=comment_id)

        if comment is None:
            return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != comment.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        comment.delete()
        return {}, HTTPStatus.NO_CONTENT


class CommentPublishResource(Resource):

    @jwt_required
    def put(self, comment_id):

        comment = Comment.get_by_id(comment_id=comment_id)

        if comment is None:
            return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != comment.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        comment.is_publish = True
        comment.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, comment_id):

        comment = Comment.get_by_id(comment_id=comment_id)

        if comment is None:
            return {'message': 'Comment not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != comment.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        comment.is_publish = False
        comment.save()

        return {}, HTTPStatus.NO_CONTENT
