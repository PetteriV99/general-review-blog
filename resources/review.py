from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.review import Review
from schemas.review import ReviewSchema

review_schema = ReviewSchema()
review_list_schema = ReviewSchema(many=True)

# comments
from models.comment import Comment
from schemas.comment import CommentSchema

comment_schema = CommentSchema()
comment_list_schema = CommentSchema(many=True)


class ReviewListResource(Resource):

    def get(self):

        reviews = Review.get_all_published()

        return review_list_schema.dump(reviews).data, HTTPStatus.OK     # returns reviews

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = review_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        review = Review(**data)
        review.user_id = current_user

        review.save()

        return review_schema.dump(review).data, HTTPStatus.CREATED


# returns all published comments in a review
class ReviewCommentListResource(Resource):
    def get(self, review_id):

        comments = Comment.get_all_published_comments(review_id=review_id)
        return comment_list_schema.dump(comments).data, HTTPStatus.OK

    @jwt_required
    def post(self, review_id):

        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = comment_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        comment = Comment(**data)
        comment.user_id = current_user  # assigns user id for comment
        comment.review_id = review_id   # assigns review id for comment
        comment.save()

        return comment_schema.dump(comment).data, HTTPStatus.CREATED


class ReviewResource(Resource):

    @jwt_optional
    def get(self, review_id):

        review = Review.get_by_id(review_id=review_id)  # finds review

        if review is None:
            return {'message': 'Review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if review.is_publish == False and review.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return review_schema.dump(review).data, HTTPStatus.OK

    @jwt_required
    def patch(self, review_id):

        json_data = request.get_json()

        data, errors = review_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        review = Review.get_by_id(review_id=review_id)

        if review is None:
            return {'message': 'Review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != review.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        review.title = data.get('title') or review.title
        review.content = data.get('content') or review.content
        review.rating = data.get('rating') or review.rating

        review.save()

        return review_schema.dump(review).data, HTTPStatus.OK

    @jwt_required
    def delete(self, review_id):

        review = Review.get_by_id(review_id=review_id)

        if review is None:
            return {'message': 'Review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != review.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        review.delete()

        return {}, HTTPStatus.NO_CONTENT


class ReviewCommentResource(Resource):

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
        comment.review_helpful = data.get('review_helpful') or comment.review_helpful

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


class ReviewPublishResource(Resource):

    @jwt_required
    def put(self, review_id):

        review = Review.get_by_id(review_id=review_id)

        if review is None:
            return {'message': 'Review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != review.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        review.is_publish = True
        review.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, review_id):

        review = Review.get_by_id(review_id=review_id)

        if review is None:
            return {'message': 'Review not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != review.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        review.is_publish = False
        review.save()

        return {}, HTTPStatus.NO_CONTENT


class ReviewCommentPublishResource(Resource):

    @jwt_required
    def put(self, review_id, comment_id):

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
