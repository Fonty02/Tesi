"""
The collection of global configurations
"""
CONFIG = {
	'DATASETS':				[
								'amazon_books_60core_kg',
								'mind',
								'movielens'
							],
	'MODELS':				[
								# General Recommendation
								'ItemKNN',
								'Pop',
								# Matrix fact & Linear
								'BPR',
								'DMF',
								'SLIMElastic',
								# Deep Learning-based
								'MultiDAE',
								'NGCF',
								'DGCF',
								# Graph-based
								'LightGCN',
								'SGL',
								# Knowledge-aware
								'CKE',
								'CFKG',
								'MKR',
								'KGCN',
								'KTUP',
								'RippleNet'
							],
	'LOG_FILE':				'log/carbon.log',
	'RESULT_PATH':			'results/',
	'RESULT_FILE':			'/emissions.csv',
	'STATIC_CONFIG_PATH':	'config/static/',
	'HP_CONFIG_PATH':		'config/hyperparam/',
}


def get_global_config():
	"""
	The getter method
	"""
	return CONFIG


def set_global_config(key, value):
	"""
	The setter method
	"""
	CONFIG.update({key: value})