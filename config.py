class Config(object):
    DEBUG = False
    TESTING = False

class Production(Config):
    pass

class Development(Config):
    DEBUG = True

class Testing(Config):
    TESTING = True

class Default(Config):
    MONGO_URI = 'mongodb://127.0.0.1:27017/mikroblog'
