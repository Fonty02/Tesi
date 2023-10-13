
from codecarbon import EmissionsTracker
from recbole.quick_start import run_recbole
import sys
import os
from recbole.quick_start import load_data_and_model
import pandas as pd
from recbole.data.interaction import Interaction
from recbole.utils import get_trainer
import csv
import json
import time


def process(dataset, model, counter):

	# check weather performances have been already computed	skip = False

	list_metrics_file = os.listdir('results/'+dataset+'/')
	for file in list_metrics_file:
		if model in file:
			skip = True

	if skip:
		print('skipping', dataset, model)
		exit(0)

	# check weather the model has been already trained and get model name
	skip_train = False
	model_path = ''
	for file in os.listdir('saved/'+dataset+'/'):
		if model in file:
			skip_train = True
			model_path = 'saved/'+dataset+'/'+file
			break

	# log for the current dataset
	log = open('carbon_log_'+dataset+'.log', 'a', encoding='utf-8')
	log.write('New experiment session started.')

	proj_name = str(counter)+'_'+model+'_'+dataset
	print('executing', proj_name)
	

	try:

		if model == 'movielens' or model == 'mind':

			parameter_dict = {
				'epochs': 50,
				'checkpoint_dir': 'saved/'+dataset+'/',
				'benchmark_filename': ['train', 'valid', 'test'],
				'metrics':  [ 'Recall', 'MRR', 'NDCG', 'Hit', 'MAP', 
					'Precision', 'GAUC', 'ItemCoverage', 'AveragePopularity', 'GiniIndex',
					'ShannonEntropy', 'TailPercentage']
			}

		elif model == 'mind':

			# repeatble: True ensures a fixed and automatic splitting
			parameter_dict = {
				'epochs': 50,
				'checkpoint_dir': 'saved/'+dataset+'/',
				'repeatable': True,
				'metrics':  [ 'Recall', 'MRR', 'NDCG', 'Hit', 'MAP', 
					'Precision', 'GAUC', 'ItemCoverage', 'AveragePopularity', 'GiniIndex',
					'ShannonEntropy', 'TailPercentage']
			}

		elif model == 'amazon_books_60core_kg':

			parameter_dict = {

				'epochs': 20,
				'embedding_size': 8,
				'kg_embedding_size': 8,
				'checkpoint_dir': 'saved/'+dataset+'/',
				'repeatable': True,
				'metrics':  [ 'Recall', 'MRR', 'NDCG', 'Hit', 'MAP', 
						'Precision', 'GAUC', 'ItemCoverage', 'AveragePopularity', 'GiniIndex',
						'ShannonEntropy', 'TailPercentage']
			}

		else:

			print('wrong dataset, exiting')
			exit(0)

		if not skip_train:

			# start tracking emissions
			with EmissionsTracker(project_name=proj_name, output_file='emissions_'+dataset+'.csv') as tracker:
				tracker.start()

				# train model
				run_recbole(model=model, dataset=dataset, config_dict=parameter_dict)
				tracker.stop()
				codecarbon_results = vars(tracker)

			log_str = 'EXECUTED: ' + proj_name + '\n'
			log.write(log_str)
			log.flush()
			print(log_str)		

			# get model name
			all_models = os.listdir('saved/'+dataset+'/')
			for m in all_models:
				if model in m:
					model_path = 'saved/'+dataset+'/'+m
					break

			print(model_path)

		# compute metrics
		config, model_pth, dataset_pth, train_data, valid_data, test_data = load_data_and_model(model_path)
		trainer = get_trainer(config['MODEL_TYPE'], config['model'])(config, model_pth)
		trainer.eval_collector.data_collect(train_data)
		trainer.saved_model_file = model_path
		metrics = trainer.evaluate(test_data)

		# save results
		name_out1 = 'results/'+dataset+'/codecarbon_'+model_path.split('/')[-1].replace('.pth','.tsv')
		name_out2 = 'results/'+dataset+'/recbole_'+model_path.split('/')[-1].replace('.pth','.tsv')

		with open(name_out1, "w") as outfile:
		    csvwriter = csv.writer(outfile, delimiter='\t')
		    csvwriter.writerow(dict(codecarbon_results))
		    csvwriter.writerow(dict(codecarbon_results).values())

		with open(name_out2, 'w') as outfile:
		    csvwriter = csv.writer(outfile, delimiter='\t')
		    csvwriter.writerow(dict(metrics))
		    csvwriter.writerow(dict(metrics).values())

	except Exception as e:	

		log_str = 'ERROR: ' + proj_name + '. ' + str(e) + '\n'
		log.write(log_str)
		log.flush()
		print(log_str)	

	log.flush()
	log.close()


if __name__ == "__main__":

	args = sys.argv[1:]
	dataset = args[0].split('=')[1]
	model = args[1].split('=')[1]
	counter = int(args[2].split('=')[1])
	
	process(dataset, model, counter)