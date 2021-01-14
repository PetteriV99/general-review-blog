from extensions import db


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(512), nullable=False)
    review_helpful = db.Column(db.Boolean(), default=True)

    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    review_id = db.Column(db.Integer(), db.ForeignKey("review.id"))

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()

    @classmethod
    def get_all_published_comments(cls, review_id):  # review id so we can find all comments of a review
        return cls.query.filter_by(is_publish=True, review_id=review_id).all()

    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_id(cls, comment_id):
        return cls.query.filter_by(id=comment_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()