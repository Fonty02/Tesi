"""
A collection of utility functions
"""
import os
from pathlib import Path
import torch
import csv
from datetime import datetime
from functools import reduce


def create_folders(datasets, models, first_level_folders):
	"""Create folder structure in this order:
		│
		├── first_level_folders
		│   │
		│   └── datasets
		│   	│
		│   	└── models
	Args:
	first_level_folders: folders root in which create structure
	datasets: first level subfolders
	models: second level subfolders
	"""
	for f in first_level_folders:
		for d in datasets:
			path_base = os.path.join(f, d)
			if not os.path.isdir(path_base):
				Path(path_base).mkdir(parents=True, exist_ok=True)
			for m in models:
				path_full = os.path.join(path_base, m)
				if not os.path.isdir(path_full):
					Path(path_full).mkdir(parents=True, exist_ok=True)


def get_device():
	"""Returns the device available on the current machine
	Args: None
	"""
	device = 'cpu'
	# Macos GPU
	if torch.backends.mps.is_available():
		device = 'mps'
	# Cuda GPU
	elif torch.cuda.is_available():
		device = 'cuda'
	return device


def write_dict_to_csv(file, my_dict):
	"""Write to csv file the given dictionary
	Args:
	file: file's path
	my_dict: data to be written
	"""
	if os.path.isfile(file):
		with open(file, 'a', encoding='utf-8') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',')
			csvwriter.writerow(my_dict.values())
	else:
		with open(file, 'w', encoding='utf-8') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',')
			csvwriter.writerow(my_dict)
			csvwriter.writerow(my_dict.values())


def get_date_time():
	"""Returns the current date in datetime format
	Args: None
	"""
	ts = datetime.timestamp(datetime.now())
	date_time = datetime.fromtimestamp(ts)
	return date_time.strftime("%Y-%m-%d %H:%M:%S")


def get_total_iterations(file):
	"""Returns the total number of iterations according to the grid-search
	Args:
	file: cofiguration's file (.hyper)
	"""
	lenghts = []
	with open(file, "r") as fp:
		for line in fp:
			para_list = line.strip().split(" ")
			if len(para_list) < 3:
				continue
			lenghts.append(len(eval("".join(para_list[2:]))))
	return reduce(lambda x, y: x * y, lenghts)
