"""
A collection of plotting functions
"""
import matplotlib.pyplot as plt
from utils import get_total_iterations
import numpy as np


def plot_results(results, experiments, hp_config_path):
	"""Plots the emissions and avg. emissions for each model.
	Args:
		results (dict): Dictionary with results (see get_hp_outcome() in helper/utils.py).
		experiments (list): List of experiments (see get_hp_outcome() in helper/utils.py).
		hp_config_path (str): The configuration's file path (.hyper).
	Returns:
		None.
	"""
	labels_x2 = [l.split('/')[1] for l in experiments]
	features_to_plot2 = {
		'total_emissions': results['emissions'],
		'avg_emissions': [v / get_total_iterations(hp_config_path + labels_x2[i] + ".hyper") for i, v in enumerate(results['emissions'])]}
	x1 = np.arange(len(labels_x2))  # the label locations
	width = 0.5  # the width of the bars
	multiplier = 0
	fig, axs = plt.subplots(1, 2, figsize=(18, 8))
	for i, v in enumerate(features_to_plot2.keys()):
		for attribute, measurement in [(v, features_to_plot2[v])]:
			offset = width * multiplier
			rects = axs[i].bar(x1 + offset, [round(i, 3) for i in measurement], width, label = attribute)
			axs[i].bar_label(rects, padding = 3)
			multiplier += 1
		axs[i].set_xlabel('Models', fontsize=14)
		axs[i].set_ylabel('Emissions (g)', fontsize=14)
		axs[i].set_title(v.capitalize() + ' by model', fontsize=18)
		axs[i].set_xticks(x1 + (i / 2), labels_x2, rotation = 60, ha="right")
	fig.tight_layout()
	plt.show()


def plot_tradeoff(results, metrics, experiments):
	"""Plots the trade-off between best metrics and total emissions.
	Args:
		results (dict): Dictionary with results (see get_hp_outcome() in helper/utils.py).
		metrics (dict): Dictionary with metrics (see get_hp_outcome() in helper/utils.py).
		experiments (list): List of experiments (see get_hp_outcome() in helper/utils.py).
	Returns:
		None.
	"""
	counter = 0
	l = [['emissions','recall@10'],['emissions','ndcg@10'],['emissions','averagepopularity@10'],['emissions','giniindex@10']]
	fig, axs = plt.subplots(2, 2, figsize=(18, 12))
	for _, axl in enumerate(axs):
		for _, ax in enumerate(axl):
			ax.scatter(results[l[counter][0]], metrics[l[counter][1]], s=80)
			ax.set_title(l[counter][0]+' X '+l[counter][1], fontsize=18)
			ax.set_xlabel(l[counter][0] + ' (g, log base2)', fontsize=14)
			ax.set_ylabel(l[counter][1], fontsize=14)
			ax.grid()
			for i, (xi, yi) in enumerate(zip(results[l[counter][0]], metrics[l[counter][1]])):
				ax.text(xi+.001, yi+.001, experiments[i].split('/')[1], fontsize=14)
			ax.set_xscale('log', base=2)
			counter = counter + 1
	fig.tight_layout()
	plt.show()


def plot_tradeoff_by_increment(best, experiments):
	"""Plots the trade-off between increments and best-run emissions.
	Args:
		best (dict): Dictionary with best-run results (see get_hp_outcome() in helper/utils.py).
		experiments (list): List of experiments (see get_hp_outcome() in helper/utils.py).
	Returns:
		None.
	"""
	counter = 0
	l = ['recall@10', 'ndcg@10', 'averagepopularity@10', 'giniindex@10']
	fig, axs = plt.subplots(2, 2, figsize=(18, 12))
	for _, axl in enumerate(axs):
		for _, ax in enumerate(axl):
			ax.scatter(best[l[counter]]['emissions'], best[l[counter]]['increments'], s=80)
			ax.set_title(l[counter], fontsize=18)
			ax.set_xlabel('best model emissions (g, log base2)', fontsize=14)
			ax.set_ylabel('increment (%)', fontsize=14)
			ax.grid()
			for i, (xi, yi) in enumerate(zip(best[l[counter]]['emissions'], best[l[counter]]['increments'])):
				ax.text(xi+.001, yi+.001, experiments[i].split('/')[1], fontsize=14)
			ax.set_xscale('log', base=2)
			counter = counter + 1
	fig.tight_layout()
	plt.show()


def plot_power(results, experiments):
	"""Plots the power consuption for each component.
	Args:
		results (dict): Dictionary with results (see get_hp_outcome() in helper/utils.py).
		experiments (list): List of experiments (see get_hp_outcome() in helper/utils.py).
	Returns:
		None.
	"""
	labels_x1 = [l.split('/')[1] for l in experiments]
	features_to_plot1 = {'CPU': results['cpu_power'], 'GPU': results['gpu_power'], 'RAM': results['ram_power']}
	x1 = np.arange(len(labels_x1))  # the label locations
	width = 0.2  # the width of the bars
	multiplier = 0
	fig, ax1 = plt.subplots(1, 1, figsize=(18, 8))
	for attribute, measurement in features_to_plot1.items():
		offset = width * multiplier
		rects = ax1.bar(x1 + offset, [round(i, 0) for i in measurement], width, label = attribute)
		ax1.bar_label(rects, padding = 3)
		multiplier += 1
	ax1.set_xlabel('Models', fontsize=14)
	ax1.set_ylabel('Power (W)', fontsize=14)
	ax1.set_title('Power consuption by component', fontsize=18)
	ax1.set_xticks(x1 + (width), labels_x1)
	ax1.legend(loc = 'upper right', ncol = 2)
	fig.tight_layout()
	plt.show()


def plot_increments_by_metrics(best):
	"""Plots the avg. increment for each metric.
	Args:
		best (dict): Dictionary with best-run results (see get_hp_outcome() in helper/utils.py).
	Returns:
		None.
	"""
	avg_increments = {}
	for _, v in enumerate(best.keys()):
		avg_increments[v] = sum(best[v]['increments']) / len(best[v]['increments'])
	x1 = np.arange(len(list(avg_increments.keys())))  # the label locations
	width = 0.5  # the width of the bars
	multiplier = 0
	fig, ax = plt.subplots(1, 1, figsize=(18, 10))
	for attribute, measurement in [('', list(avg_increments.values()))]:
		offset = width * multiplier
		rects = ax.bar(x1 + offset, [round(i, 0) for i in measurement], width, label = attribute)
		ax.bar_label(rects, padding = 3)
		multiplier += 1
	ax.set_xlabel('Metrics', fontsize=14)
	ax.set_ylabel('Increments (%)', fontsize=14)
	ax.set_title('Avg. increments by metrics', fontsize=18)
	ax.set_xticks(x1, list(avg_increments.keys()), rotation = 60, ha="right")
	fig.tight_layout()
	plt.show()