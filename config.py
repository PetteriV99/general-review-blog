class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'petteri:Salasana12@localhost:5432/general-blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    UPLOADED_IMAGES_DEST = 'static/images'
