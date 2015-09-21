import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '/B]\x06L.\xab\xa4^\x93:}\xc2\x13\xbea\xaa\xcc\x1c\x1f5vq\xad'
    DEBUG = False
    # Oauth configuration data
    GOOGLE_LOGIN_CLIENT_ID = "727826238640-1r785tt8jreu352n95f37" \
                             "fgpkn9hrsvs.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "wWV18P3ZZASuMxeQruCezFZQ"
    FACEBOOK_LOGIN_CLIENT_ID = "519207281561864"
    FACEBOOK_LOGIN_CLIENT_SECRET = "ca811981954aff3b468941dbe5c325b7"

    OAUTH_CREDENTIALS = {
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        },
        'facebook': {
            'id': FACEBOOK_LOGIN_CLIENT_ID,
            'secret': FACEBOOK_LOGIN_CLIENT_SECRET
        }
    }


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'catalog.db')


class TestingConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'data-test.db')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'catalog.db')

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
