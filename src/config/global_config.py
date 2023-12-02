"""
The collection of global configurations
"""
CONFIG = {
	'DATASETS':				[
								'amazon_books_60core_kg',
								'mind',
								'movielens100k',
								'movielens1m'
							],
	'MODELS':				[
								# General Recommendation
								'ItemKNN',
								'Pop',
								'Random',
								'SimpleX',
								# Matrix fact & Linear
								'ADMMSLIM',
								'BPR',
								'DMF',
								'ENMF',
								'FISM',
								'NCEPLRec',
								'SLIMElastic',
								# Deep Learning-based
								'CDAE',
								'ConvNCF',
								'DiffRec',
								'EASE',
								'GCMC',
								'LDiffRec',
								'MacridVAE',
								'MultiDAE',
								'MultiVAE',
								'NAIS',
								'NeuMF',
								'NGCF',
								'NNCF',
								'LightGCN',
								'RaCT',
								'RecVAE',
								# Graph-based
								'DGCF',
								'LINE',
								'NCL',
								'SGL',
								'SpectralCF',
								# Knowledge-aware
								'CKE',
								'CFKG',
								'KGAT',
								'KGCN',
								'KGIN',
								'KGNNLS',
								'KTUP',
								'MCCLK',
								'MKR',
								'RippleNet'
							],
	'LOG_FILE':				'log/carbon.log',
	'RESULT_PATH':			'results/',
	'EMISSIONS_FILE':		'/emissions.csv',
	'METRICS_FILE':			'/metrics.csv',
	'PARAMS_FILE':			'/params.csv',
	'STATIC_CONFIG_FILE':	'src/config/_params.yaml',
	'HP_CONFIG_PATH':		'src/config/hyperparam/',
	'COUNTER':				1
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