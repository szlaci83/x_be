class BaseConf(object):
    DB_NAME = "example"
    DEFAULT_PAGESIZE = 21
    HOST = "0.0.0.0"
    PORT = 4555
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_NAME + '.db'


class Dev(BaseConf):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    SSL_CONTEXT = None


class Prod(BaseConf):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SSL_CONTEXT = ('cert1.pem', 'privkey1.pem')


ENV = Dev

