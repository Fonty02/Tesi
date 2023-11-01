import sys
import os
import copy
import traceback
import yaml
from codecarbon import EmissionsTracker
from recbole.trainer import HyperTuning
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.utils import get_trainer, get_model, init_seed
from config.global_config import get_global_config
from config.params_config import get_params, set_param
from utils import create_folders, get_device, write_dict_to_csv

config = get_global_config()
config_dict = get_params()
DATASETS = config.get('DATASETS')
MODELS = config.get('MODELS')
LOG_FILE = config.get('LOG_FILE')
RESULT_PATH = config.get('RESULT_PATH')
EMISSIONS_FILE = config.get('EMISSIONS_FILE')
STATIC_CONFIG_FILE = config.get('STATIC_CONFIG_FILE')
HP_CONFIG_PATH = config.get('HP_CONFIG_PATH')
METRICS_FILE = config.get('METRICS_FILE')
PARAMS_FILE = config.get('PARAMS_FILE')


def objective_function(config_dict=None, config_file_list=None):

	config = Config(config_dict=config_dict, config_file_list=config_file_list)
	init_seed(config['seed'], reproducibility=True)
	dataset = create_dataset(config)
	train_data, valid_data, test_data = data_preparation(config, dataset)
	model = get_model(config['model'])(config, train_data._dataset).to(config['device'])
	trainer = get_trainer(config['MODEL_TYPE'], config['model'])(config, model)

	_el = config['checkpoint_dir'].split('/')
	proj_name = _el[1].upper() + '_' + _el[2].upper() + '_PARAMS_TUNING'
	results_path = os.path.join(RESULT_PATH, _el[1], _el[2])

	# Start tracking emissions
	with EmissionsTracker(
		project_name=proj_name,
		output_file=results_path + EMISSIONS_FILE,
		tracking_mode='process',
		on_csv_write='update'
	) as tracker:
		tracker.start()
		best_valid_score, best_valid_result = trainer.fit(train_data, valid_data, verbose=False)
		tracker.stop()
		codecarbon_results = dict(vars(tracker))
	test_result = trainer.evaluate(test_data)

	# Save results
	metrics = dict(test_result)
	full_params = dict(config._get_final_config_dict())
	metrics['run_id'] = codecarbon_results['run_id']
	metrics['project_name'] = proj_name
	full_params['run_id'] = codecarbon_results['run_id']
	full_params['project_name'] = proj_name
	write_dict_to_csv(results_path + METRICS_FILE, metrics)
	write_dict_to_csv(results_path + PARAMS_FILE, full_params)

	return {
		'model': config['model'],
		'best_valid_score': best_valid_score,
		'valid_score_bigger': config['valid_metric_bigger'],
		'best_valid_result': best_valid_result,
		'test_result': test_result
	}


def process(dataset, model):

	# Create directory structure is not already exists
	_saved = copy.deepcopy(config_dict.get('checkpoint_dir'))
	create_folders([dataset], [model], [RESULT_PATH, _saved])

	# Log for the current dataset
	log = open(LOG_FILE, 'a', encoding='utf-8')
	log.write('New experiment session started.')
	proj_name = dataset.upper() + '_' + model.upper() + '_PARAMS_TUNING'
	print('executing', proj_name)

	# Setup runtime config
	pth = os.path.join(config_dict.get('checkpoint_dir'), dataset, model)
	set_param('checkpoint_dir', pth)
	set_param('dataset', dataset)
	set_param('model', model)
	set_param('device', get_device())

	try:
		with open(STATIC_CONFIG_FILE, 'w', encoding='utf-8') as yaml_output:
			yaml.dump(config_dict, yaml_output, sort_keys=False)

		hp = HyperTuning(
			objective_function=objective_function,
			algo='exhaustive',
			params_file=HP_CONFIG_PATH + model + '.hyper',
			fixed_config_file_list=[STATIC_CONFIG_FILE]
		)
		hp.run()

		if os.path.isfile(STATIC_CONFIG_FILE):
			os.unlink(STATIC_CONFIG_FILE)
		log_str = 'EXECUTED: ' + proj_name + '\n'
		log.write(log_str)
		log.flush()
		print(log_str)

	except Exception as e:
		print(traceback.format_exc())
		log_str = 'ERROR: ' + proj_name + '. ' + str(e) + '\n'
		log.write(log_str)
		log.flush()
		print(log_str)

	log.flush()
	log.close()

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) == 0:
		print('\nWARNING: missing required parameters!')
		print('\n' + ''.join(['> ' for i in range(25)]))
		print(f'\n{"PARAM":<16}{"VALUE RANGE":<18}\n')
		print(''.join(['> ' for i in range(25)]))
		print(f'{"--dataset":<16}{DATASETS:<18}')
		print(f'{"--model":<16}{MODELS:<18}')
		print(''.join(['> ' for i in range(25)]) + '\n')
	else:
		keys = [i.split('=')[0].upper()[2:] for i in args]
		values = [i.split('=')[1] for i in args]
		if 'DATASET' in keys and 'MODEL' in keys:
			dataset = values[keys.index('DATASET')]
			model = values[keys.index('MODEL')]
			if dataset not in DATASETS:
				print('WARNING: invalid DATASET value!')
				print('Valid: ', DATASETS)
			elif model not in MODELS:
				print('WARNING: invalid MODEL value!')
				print('Valid: ', MODELS)
			else:
				process(dataset, model)
		else:
			print('WARNING: required arguments are missing!')
			if 'DATASET' not in keys:
				print('MISSING: DATASET=""')
			if 'MODEL' not in keys:
				print('MISSING: MODEL=""')
	sys.exit(0)