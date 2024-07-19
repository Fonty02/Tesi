import os
import shutil
import time
import gc
import torch


#models = ['BPR', 'CFKG', 'CKE', 'DMF', 'KGCN', 'KGNNLS', 'LINE', 'MultiDAE', 'LightGCN', 'NGCF', 'DGCF']
#models = ['BPR', 'DMF', 'LINE', 'MultiDAE', 'LightGCN', 'NGCF', 'DGCF']
models=['DMF']
datasets = ['movielens_1m']
max_emission_step = 7
ratio_tolerance =40
#clear with gc and cuda
for dataset in datasets:
    for model in models:
        os.system(f"python src/default_tracker2.py --dataset={dataset} --model={model} --max_emission_step={max_emission_step} --ratio_tolerance={ratio_tolerance}")
        #os.system(f"python src/default_tracker.py --dataset={dataset} --model={model}")
        time.sleep(30)