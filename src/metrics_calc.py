import sys
import os
from sys import platform
from recbole.quick_start import load_data_and_model
from recbole.utils import get_trainer
from config.global_config import get_global_config
from config.params_config import get_params, set_param
from utils import get_device, write_dict_to_csv
import gc
import torch


config = get_global_config()
config_dict = get_params()
DATASETS = config.get('DATASETS')
MODELS = config.get('MODELS')
CHECKPOINT_DIR = config_dict.get('checkpoint_dir')
BASE_PATH = '/'.join(os.getcwd().split('/'))
LOG_FILE = os.path.join(BASE_PATH, config.get('LOG_FILE_DEFAULT'))
RESULT_PATH = os.path.join(BASE_PATH, config.get('RESULT_PATH_SHARED2'))
if platform == 'win32':
	BASE_PATH = BASE_PATH.replace('/', '\\')
	LOG_FILE = LOG_FILE.replace('/', '\\')
	RESULT_PATH = RESULT_PATH.replace('/', '\\')
METRICS_FILE = config.get('METRICS_FILE')
metrics=['Recall','MRR','NDCG','Hit','MAP','Precision','GAUC','ItemCoverage','AveragePopularity','GiniIndex','ShannonEntropy','TailPercentage']




def calc_metrics(dataset,model,metrics):
	pth = os.path.join(config_dict.get('checkpoint_dir'), dataset, model)
	set_param('checkpoint_dir', pth)
	set_param('dataset', dataset)
	set_param('model', model)
	set_param('device', get_device())
	set_param('my_log_file', LOG_FILE)
	results_path = os.path.join(RESULT_PATH, dataset, model)
	model_saved = os.path.join(pth, sorted(os.listdir(pth))[-1])
	config_rec, model_rec, _, train_data, _, test_data = load_data_and_model(model_saved)
	config_rec['metrics'] = metrics
	#trai the model calculating the metrics in metrics
	trainer = get_trainer(config_rec['MODEL_TYPE'], config_rec['model'])(config_rec, model_rec)
	trainer.eval_collector.data_collect(train_data)
	met = trainer.evaluate(test_data, model_file=model_saved)
	met = dict(met)
	#rename this file "results_path + METRICS_FILE" into "results_path + METRICS_FILE + "2"
    #write the metrics in met into "results_path + METRICS_FILE"
	#os.rename(results_path + METRICS_FILE, results_path + METRICS_FILE + "2")
	write_dict_to_csv(results_path + METRICS_FILE,met)
	del config_rec, model_rec, train_data, test_data, trainer, metrics,met
	gc.collect()
	torch.cuda.empty_cache()
	





if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) == 0:
		calc_metrics('movielens_1m', 'DGCF',metrics)
	else:
		keys = [i.split('=')[0].upper()[2:] for i in args]
		values = [i.split('=')[1] for i in args]
		if 'DATASET' in keys and 'MODEL' in keys:
			dataset = values[keys.index('DATASET')]
			model = values[keys.index('MODEL')]
			'''if dataset not in DATASETS:
				print('WARNING: invalid DATASET value!')
				print('Valid: ', DATASETS)
			elif model not in MODELS:
				print('WARNING: invalid MODEL value!')
				print('Valid: ', MODELS)
			else:'''
			calc_metrics(dataset, model,metrics)
		else:
			print('WARNING: required arguments are missing!')
			if 'DATASET' not in keys:
				print('MISSING: DATASET=""')
	sys.exit(0)