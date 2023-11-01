import os
from pathlib import Path


def create_folders(datasets, models, first_level_folders):
	for f in first_level_folders:
		for d in datasets:
			path_base = os.path.join(f, d)
			if not os.path.isdir(path_base):
				Path(path_base).mkdir(parents=True, exist_ok=True)
			for m in models:
				path_full = os.path.join(path_base, m)
				if not os.path.isdir(path_full):
					Path(path_full).mkdir(parents=True, exist_ok=True)