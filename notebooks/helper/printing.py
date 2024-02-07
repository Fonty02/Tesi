"""
A collection of printing functions
"""
import datetime
from utils import get_total_iterations


def print_durations(results, experiments, hp_config_path):
	"""Prints duration, avg. duration and nr. of runs for each experiment.
	Args:
		results (dict): Dictionary with results (see get_hp_outcome() in helper/utils.py).
		experiments (list): List of experiments (see get_hp_outcome() in helper/utils.py).
		hp_config_path (str): The configuration's file path (.hyper).
	Returns:
		None.
	"""
	print(''.join(['> ' for i in range(42)]))
	print(f'\n{"ID":<5}{"DATASET":<18}{"MODEL":<10}{"RUNs":>8}{"DURATION":>20}{"AVG DURATION":>18}\n')
	print(''.join(['> ' for i in range(42)]))
	totals = []
	for i, v in enumerate(experiments):
		totals.append(results["duration"][i])
		runs = get_total_iterations(hp_config_path + v.split("/")[1] + ".hyper")
		print(f'\n{i+1:<5}{v.split("/")[0][:12]:<18}{v.split("/")[1]:<10}{runs:>8}{str(datetime.timedelta(seconds=int(results["duration"][i]))):>20}{str(datetime.timedelta(seconds=int(results["duration"][i]/runs)))[2:]:>18}')
		if i > 1 and i == len(experiments) - 1:
			print(f'\n\033[1m{"":<5}{"TOTAL:":<18}{str(datetime.timedelta(seconds=int(sum(totals)))):>36}\033[0m\n')
			totals = []


def print_best_metrics(results, best, experiments):
	"""Prints the metric/s with the lowest percentage increment for each experiment.
	Args:
		results (dict): Dictionary with results (see get_hp_outcome() in helper/utils.py).
		best (dict): Dictionary with best-run results (see get_hp_outcome() in helper/utils.py).
		experiments (list): List of experiments (see get_hp_outcome() in helper/utils.py).
	Returns:
		None.
	"""
	print(''.join(['> ' for i in range(50)]))
	print(f'\n{"ID":<5}{"DATASET":<13}{"MODEL":<12}{"BEST_METRIC by INCR.":<20}{"BEST_RUN(g)":>15}{"TOTAL(g)":>15}{"INCREMENT(%)":>15}\n')
	print(''.join(['> ' for i in range(50)]))
	for i, v in enumerate(experiments):
		increments = [best[m]["increments"][i] for m in best.keys()]
		min_keys = [i for i, x in enumerate(increments) if x == min(increments)]
		for j, k in enumerate(best.keys()):
			if j in min_keys:
				print(f'{i+1:<5}{v.split("/")[0][:12]:<13}{v.split("/")[1]:<12}{k:<20}{best[k]["emissions"][i]:>15.4f}{results["emissions"][i]:>15.3f}{best[k]["increments"][i]:15.0f}')
		print('')