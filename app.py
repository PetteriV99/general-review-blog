from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_uploads import configure_uploads, patch_request_class

from config import Config
from extensions import db, jwt, image_set


from resources.user import UserListResource, UserResource, MeResource, UserReviewListResource, UserActivateResource, UserAvatarUploadResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
from resources.review import ReviewListResource, ReviewResource, ReviewPublishResource

from resources.comment import CommentListResource, CommentResource, CommentPublishResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    configure_uploads(app, image_set)
    patch_request_class(app, 10 * 1024 * 1024)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list


def register_resources(app):

    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')
    api.add_resource(UserReviewListResource, '/users/<string:username>/reviews')

    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(ReviewListResource, '/reviews')
    api.add_resource(ReviewResource, '/reviews/<int:review_id>')
    api.add_resource(ReviewPublishResource, '/reviews/<int:review_id>/publish')

    #api.add_resource(CommentListResource, '/reviews/<int:review_id>/comments')
    #api.add_resource(CommentResource, '/reviews/<int:review_id>/comments/<int:comment_id>')
    #api.add_resource(CommentPublishResource, '/reviews/<int:review_id>/comments/<int:comment_id>/publish')

    api.add_resource(CommentListResource, '/comments')
    api.add_resource(CommentResource, '/comments/<int:comment_id>')
    api.add_resource(CommentPublishResource, '/comments/<int:comment_id>/publish')

if __name__ == '__main__':
    app = create_app()
    CORS(app)
    app.run()
