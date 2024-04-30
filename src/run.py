import os
import shutil
import time




#models = ['ItemKNN','BPR', 'CFKG', 'CKE', 'DMF', 'KGCN', 'KGNNLS', 'LINE', 'MultiDAE', 'LightGCN']
datasets = ['ml-100k']
models=['BPR']
max_emission = 1e-4
for dataset in datasets:
    for model in models:
        os.system(f"python src/default_tracker2.py --dataset={dataset} --model={model} --max_emission={max_emission}")
        time.sleep(5)