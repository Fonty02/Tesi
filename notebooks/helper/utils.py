"""
A collection of utility functions
"""
import os
import pandas as pd


def get_hp_outcome(dataset, result_path, emissions_file='emissions.csv', metrics_file='metrics.csv'):
	"""Get the results of the hyperparameter tuning.
	Args:
		dataset (str): A valid dataset name (see src/config/global_config.py).
		result_path (str): The folder were the results are stored.
		emissions_file (str): Filename containing emissions.
		metrics_file (str): Filename containing metrics.
	Returns:
		results (dict): Total results of the hyperparameter tuning.
		metrics (dict): All the metrics computed.
		experiments (list): List of the experiments conducted.
		best (dict): Results relative to the best run.
	"""
	experiments = []
	for m in next(os.walk(result_path + dataset))[1]:
		experiments.append(os.path.join(dataset, m))
	experiments = sorted(experiments)

	metrics_max = ['recall@10', 'mrr@10', 'ndcg@10', 'hit@10', 'map@10', 'precision@10', 'gauc', 'itemcoverage@10', 'shannonentropy@10']
	metrics_min = ['averagepopularity@10', 'giniindex@10']
	results = {'emissions': [], 'duration': [], 'cpu_power': [], 'gpu_power': [], 'ram_power': []}
	metrics = {}
	best = {} # best contains the emissions of the best run by metric for each model
	for m in (metrics_max + metrics_min):
		metrics[m] = []
		best[m] = {'emissions': [], 'increments': []}

	for _, v in enumerate(experiments):
		emissions_df = pd.read_csv(os.path.join(result_path, v, emissions_file))
		metrics_df = pd.read_csv(os.path.join(result_path, v, metrics_file))
		e = emissions_df[
			['project_name', 'duration', 'emissions', 'cpu_power', 'gpu_power', 'ram_power']
		].groupby(['project_name']).sum()
		m_max = metrics_df[['project_name'] + metrics_max].groupby(['project_name']).max()
		m_min = metrics_df[['project_name'] + metrics_min].groupby(['project_name']).min()
		m = m_max.merge(m_min, how='left', on='project_name')
		if len(e) > 1 or len(m) > 1:
			print('ERROR: len()>1 detected!')
			raise Exception()
		else:
			for k in results.keys():
				if k == 'emissions':
					results[k].append(e.iloc[0][k] * 1000)
				else:
					results[k].append(e.iloc[0][k])
			for k in metrics.keys():
				metrics[k].append(m.iloc[0][k])
				if k in metrics_max:
					run_id_max = metrics_df.loc[metrics_df[k].idxmax(), 'run_id']
				else:
					run_id_max = metrics_df.loc[metrics_df[k].idxmin(), 'run_id']
				query = emissions_df[emissions_df['run_id'] == run_id_max]
				best[k]['emissions'].append(query.iloc[0]['emissions'] * 1000)
				best[k]['increments'].append(
					(results["emissions"][-1] - best[k]['emissions'][-1]) / best[k]['emissions'][-1] * 100
				)
	return results, metrics, experiments, best


def get_outcome(
		dataset,
		models,
		result_path,
		machine='azure',
		emissions_file='emissions.csv',
		metrics_file='metrics.csv'
	):
	"""Get the results of executions with default parameters.
	Args:
		dataset (str): A valid dataset name (see src/config/global_config.py).
		models (list): A list of models of interest.
		result_path (str): The folder were the results are stored.
		machine (str): An identifier of the hardware of interest.
		emissions_file (str): Filename containing emissions.
		metrics_file (str): Filename containing metrics.
	Returns:
		results (dict): Executions results.
		metrics (dict): All the metrics computed.
		experiments (list): List of the experiments conducted.
	"""
	experiments = []
	for m in next(os.walk(result_path + dataset))[1]:
		print(m)
		if m in models:
			e = pd.read_csv(os.path.join(result_path, dataset, m, emissions_file))
			if len(e[e['os'].str.contains(machine)]):
				experiments.append(os.path.join(dataset, m))
	experiments = sorted(experiments)
	metrics_list = ['recall@10', 'ndcg@10','averagepopularity@10', 'giniindex@10']
	results = {'emissions': [], 'duration': [], 'cpu_power': [], 'gpu_power': [], 'ram_power': []}
	metrics = {}
	for m in metrics_list:
		metrics[m] = []
	for _, v in enumerate(experiments):
		e = pd.read_csv(os.path.join(result_path, v, emissions_file))
		m = pd.read_csv(os.path.join(result_path, v, metrics_file))
		e = e[e['os'].str.contains(machine)]
		m = m[m['run_id'] == e.iloc[0]['run_id']]
		for k in results.keys():
			if k == 'emissions':
				results[k].append(e.iloc[0][k]*1000)
			else:
				results[k].append(e.iloc[0][k])
		for k in metrics.keys():
			metrics[k].append(m.iloc[0][k])
	return results, metrics, experiments