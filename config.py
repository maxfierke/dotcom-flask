class Config(object):
	MONGODB_SETTINGS = {
		'DB': 'mfcom'
	}

class ProdConfig(Config):
	DEBUG = False
	SECRET_KEY = 'g7sg78hiwegrujdfiolsdi9uoy4978erAIyufhgs'

class DevConfig(Config):
	DEBUG = True
	TESTING = True
