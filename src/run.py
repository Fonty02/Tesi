import os
import shutil
import time




models = ['ItemKNN','BPR', 'CFKG', 'CKE', 'DMF', 'KGCN', 'KGNNLS', 'LINE', 'MultiDAE', 'LightGCN']
datasets = ['ml-100k']



for dataset in datasets:
    for model in models:
        os.system(f"python src/default_tracker.py --dataset={dataset} --model={model}")
        time.sleep(60)