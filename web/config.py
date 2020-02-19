class DevelopmentConfig(object):
    """
    Development configurations
    """

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://stage_test:1234abcd@192.168.1.57:5432/stage_db'


class ProductionConfig(object):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://stage_test:1234abcd@postgres_host:5432/stage_db'


class TestingConfig(object):
    """
    testing configurations
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://stage_test:1234abcd@192.168.1.57:5432/stage_db'

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test':TestingConfig,
    'default': DevelopmentConfig
}
