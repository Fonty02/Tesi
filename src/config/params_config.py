"""
The collection of static params configurations

https://recbole.io/docs/v0.1.2/user_guide/config_settings.html

"""
DEFAULT_PARAMS =	{
						# Environment Setting
						'gpu_id': 0,
						'use_gpu': 'True',
						'seed': 42,
						'state': '', # ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
						'reproducibility': True,
						'data_path': 'data/',
						'checkpoint_dir': 'saved/',

						# Training Setting
						'epochs': 50,
						'train_batch_size': 2048,
						'learner': 'adam', # ['adam', 'sgd', 'adagrad', 'rmsprop', 'sparse_adam']
						'learning_rate': .001,
						'training_neg_sample_num': 1,
						'training_neg_sample_distribution': 'uniform', # ['uniform', 'popularity']
						'eval_step': 1,
						'stopping_step': 10,
						'clip_grad_norm': None,

						# Evaluation Setting
						'eval_setting': 'RO_RS,full', # ['TO_LS','RO_LS','TO_RS'] ['uni100','uni1000']
						'group_by_user': True, # It must be True when eval_setting is in ['RO_LS', 'TO_LS']
						'spilt_ratio': [0.8, 0.1, 0.1], # Only when eval_setting is ['RO_RS','TO_RS']
						'leave_one_num': 2, # # Only when eval_setting is ['RO_LS', 'TO_LS']
						'metrics': ['Recall', 'MRR', 'NDCG', 'Hit', 'MAP', 'Precision', 'GAUC', 'ItemCoverage', 'AveragePopularity', 'GiniIndex', 'ShannonEntropy', 'TailPercentage'],
						'topk': 10,
						'valid_metric': 'MRR@10',
						'eval_batch_size': 4096
					}


def get_params():
	"""
	The getter method
	"""
	return DEFAULT_PARAMS


def set_param(key, value):
	"""
	The setter method
	"""
	DEFAULT_PARAMS.update({key: value})