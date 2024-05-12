import os
import shutil
import time
import gc
import torch


#models = ['BPR', 'CFKG', 'CKE', 'DMF', 'KGCN', 'KGNNLS', 'LINE', 'MultiDAE', 'LightGCN', 'NGCF', 'DGCF']
models=['LightGCN']
datasets = ['amazon_books_60core_kg']
max_emission_step = -1
#clear with gc and cuda
gc.collect()
torch.cuda.empty_cache()
for dataset in datasets:
    for model in models:
        os.system(f"python src/default_tracker2.py --dataset={dataset} --model={model} --max_emission_step={max_emission_step}")
        #os.system(f"python src/default_tracker.py --dataset={dataset} --model={model}")
        time.sleep(5)