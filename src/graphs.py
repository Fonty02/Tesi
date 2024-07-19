import os

import matplotlib.scale
BASE_PATH ='/'.join(os.getcwd().split('/')[:-1])+ '/Tesi'
from config.global_config import get_global_config
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
_config = get_global_config()
RESULT_PATH = os.path.join(BASE_PATH, _config.get('RESULT_PATH_SHARED'))
RESULT_PATH2 = os.path.join(BASE_PATH, _config.get('RESULT_PATH_SHARED2'))

models = ['ItemKNN','BPR', 'CFKG', 'CKE', 'DMF', 'KGCN', 'KGNNLS', 'LINE', 'MultiDAE', 'LightGCN', 'NGCF', 'DGCF']
datasets = ['LFM-1b_artist_20U50I','LFM-1b_artist_20U50I_75strat','LFM-1b_artist_20U50I_50strat','LFM-1b_artist_20U50I_25strat']
#models=['DGCF']

metrics_list = ['recall@10', 'ndcg@10','averagepopularity@10', 'giniindex@10']

def plot_emission():
    for dataset in datasets:
        emissions_result = {}
        for model in models:
            results_path = os.path.join(RESULT_PATH, dataset, model)
            emissions = pd.read_csv(results_path + "/emissions.csv")
            emissions_result[model] = emissions.loc[0, 'emissions']
        plt.ylabel("Emissions log2")
        plt.xlabel("Models")
        plt.title(dataset.replace('_40_7',''))
        plt.xticks(rotation=35,fontsize=10)
        values=list(emissions_result.values())
        x_labels=list(emissions_result.keys())
        sorted_data = sorted(zip(values,x_labels), reverse=True)
        values, x_labels = zip(*sorted_data)
        plt.bar(x_labels, values,width=0.9)
        #reduce font size of x labels
        for i, v in enumerate(values):
            #plot the emissions on top of the bars
            plt.text(i, v + 0.000001, str(round(v, 3)), ha='center', va='bottom', fontsize=10) 
        plt.yscale(matplotlib.scale.LogScale(base=2, axis='y'))
        plt.show()
        plt.savefig(BASE_PATH + '/graphs/emissions_'+dataset+'.png')
        plt.close()
        del emissions_result, emissions
    #plot the emissions of the modified early stopping

    '''
   for dataset in datasets:
        emissions_result = {}
        for model in models:
            results_path = os.path.join(RESULT_PATH2, dataset, model)
            emissions = pd.read_csv(results_path + "/emissions.csv")
            emissions_result[model] = emissions.loc[0, 'emissions']
        plt.ylabel("Emissions log2")
        plt.xlabel("Models")
        plt.title(dataset.replace('_40_7',''))
        plt.xticks(rotation=45,fontsize=8)
        values=list(emissions_result.values())
        x_labels=list(emissions_result.keys())
        sorted_data = sorted(zip(values,x_labels), reverse=True)
        values, x_labels = zip(*sorted_data)
        plt.bar(x_labels, values,width=0.8)
        #reduce font size of x labels
        for i, v in enumerate(values):
            #plot the emissions on top of the bars
            plt.text(i, v + 0.000001, str(round(v, 4)), ha='center', va='bottom', fontsize=8) 
        plt.yscale(matplotlib.scale.LogScale(base=2, axis='y'))
        plt.show()
        plt.savefig(BASE_PATH + '/graphs2/emissions_'+dataset+'_earlyModified.png')
        plt.close()
        del emissions_result, emissions
        '''

        

def plot_metrics_comparison():
        for metric in metrics_list:
            for dataset in datasets:
                metrics_result={}
                emissions_result={}
                metrics_result2={}
                emissions_result2={}
                for model in models:

                    #CLASSIC EARLY STOPPING
                    results_path = os.path.join(RESULT_PATH, dataset, model)
                    metrics = pd.read_csv(results_path+"/metrics.csv")
                    emissions= pd.read_csv(results_path+"/emissions.csv")
                    metrics_result[model] = metrics[metric]
                    emissions_result[model] = emissions['emissions']

                    #MODIFIED EARLY STOPPING
                    results_path = os.path.join(RESULT_PATH2, dataset, model)
                    metrics2 = pd.read_csv(results_path+"/metrics.csv")
                    emissions2= pd.read_csv(results_path+"/emissions.csv")
                    metrics_result2[model] = metrics2[metric]
                    emissions_result2[model] = emissions2['emissions']

                plt.title(dataset.replace('_40_7',''))
                plt.ylabel(metric)
                plt.xlabel("Emissions log2")
                for i, model in enumerate(models):
                    plt.plot(emissions_result[model], metrics_result[model], 'o', label=model, color='blue')
                    plt.plot(emissions_result2[model], metrics_result2[model], 'o', label=model, color='red')


                    plt.legend(['Classic Early Stopping', 'Modified Early Stopping'])
                    plt.annotate(model, (emissions_result[model], metrics_result[model]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)
                    plt.annotate(model, (emissions_result2[model], metrics_result2[model]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)

                    for x1, y1, x2, y2 in zip(emissions_result[model], metrics_result[model], emissions_result2[model], metrics_result2[model]):
                        plt.plot([x1, x2], [y1, y2], color='green', linestyle='-', linewidth=0.5)


                plt.xscale(matplotlib.scale.LogScale(base=2,axis='x'))
                plt.grid(True)
                #allunga il grafico in orizzontale
                plt.gcf().set_size_inches(10, 5)



                plt.show()
                plt.savefig(BASE_PATH + '/graphs2/'+metric+'_'+dataset+'_comparison.png')
                plt.close()
                del metrics_result, metrics, metrics_result2, metrics2



def plot_metrics():
        for metric in metrics_list:
            for dataset in datasets:
                metrics_result={}
                emissions_result={}
                for model in models:
                    results_path = os.path.join(RESULT_PATH, dataset, model)
                    metrics = pd.read_csv(results_path+"/metrics.csv")
                    emissions= pd.read_csv(results_path+"/emissions.csv")
                    metrics_result[model] = metrics[metric]
                    emissions_result[model] = emissions['emissions']
                plt.title(dataset.replace('_40_7',''))
                plt.ylabel(metric)
                plt.xlabel("Emissions log2")
                for i, model in enumerate(models):
                    plt.plot(emissions_result[model], metrics_result[model], 'o', label=model, color='blue')
                    plt.annotate(model, (emissions_result[model], metrics_result[model]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)
                plt.xscale(matplotlib.scale.LogScale(base=2,axis='x'))
                plt.grid(True)
                plt.show()
                plt.savefig(BASE_PATH + '/graphs2/'+metric+'_'+dataset+'_earlyClassic.png')
                plt.close()
                del metrics_result, metrics


def print_table():

    for metric in metrics_list:
            for dataset in datasets:
                metrics_result={}
                emissions_result={}
                metrics_result2={}
                emissions_result2={}
                for model in models:

                    #CLASSIC EARLY STOPPING
                    results_path = os.path.join(RESULT_PATH, dataset, model)
                    metrics = pd.read_csv(results_path+"/metrics.csv")
                    emissions= pd.read_csv(results_path+"/emissions.csv")
                    metrics_result[model] = metrics[metric]
                    emissions_result[model] = emissions['emissions']

                    #MODIFIED EARLY STOPPING
                    results_path = os.path.join(RESULT_PATH2, dataset, model)
                    metrics2 = pd.read_csv(results_path+"/metrics.csv")
                    emissions2= pd.read_csv(results_path+"/emissions.csv")
                    metrics_result2[model] = metrics2[metric]
                    emissions_result2[model] = emissions2['emissions']

                #stampa la percentuale di riduzione di emissioni e di riduzione di performance tra i due metodi

                for model in models:
                    print(model, 'dataset:', dataset, 'metric:', metric)
                    print('Emissioni classic:', round(emissions_result[model].iloc[-1]*1000, 4))
                    print('Emissioni modified:', round(emissions_result2[model].iloc[-1]*1000, 4))
                    print('Performance classic:', metrics_result[model].iloc[-1])
                    print('Performance modified:', metrics_result2[model].iloc[-1])
                    print('Riduzione emissioni in percentuale:', round((emissions_result[model].iloc[-1]-emissions_result2[model].iloc[-1])/emissions_result[model].iloc[-1]*100, 4))
                    print('Riduzione emissioni in valore assoluto', round((emissions_result[model].iloc[-1]-emissions_result2[model].iloc[-1])*1000, 4))
                    print('Riduzione performance: in percentuale:', round((metrics_result[model].iloc[-1]-metrics_result2[model].iloc[-1])/metrics_result[model].iloc[-1]*100, 4))
                    print('Riduzione performance: in valore assoluto:', round((metrics_result[model].iloc[-1]-metrics_result2[model].iloc[-1]), 4))
                    print('\n')

                del metrics_result, metrics, metrics_result2, metrics2


def printEmissionScorePlot():
     #Print a plot where y axis is the abs(emission decrease)*100 and X axis is the abs(performance decrease)*100
    for metric in metrics_list:
            for dataset in datasets:
                metrics_result={}
                emissions_result={}
                metrics_result2={}
                emissions_result2={}
                for model in models:

                    #CLASSIC EARLY STOPPING
                    results_path = os.path.join(RESULT_PATH, dataset, model)
                    metrics = pd.read_csv(results_path+"/metrics.csv")
                    emissions= pd.read_csv(results_path+"/emissions.csv")
                    metrics_result[model] = metrics[metric]
                    emissions_result[model] = emissions['emissions']

                    #MODIFIED EARLY STOPPING
                    results_path = os.path.join(RESULT_PATH2, dataset, model)
                    metrics2 = pd.read_csv(results_path+"/metrics.csv")
                    emissions2= pd.read_csv(results_path+"/emissions.csv")
                    metrics_result2[model] = metrics2[metric]
                    emissions_result2[model] = emissions2['emissions']

                #stampa la percentuale di riduzione di emissioni e di riduzione di performance tra i due metodi
                performance_decrease = []
                emission_decrease = []
                emission_difference=[]
                performance_difference=[]
                for model in models:
                    #performance_decrease.append(abs((metrics_result[model].iloc[-1]-metrics_result2[model].iloc[-1])/metrics_result[model].iloc[-1]*100))
                    #emission_decrease.append((abs(emissions_result[model].iloc[-1]-emissions_result2[model].iloc[-1])/emissions_result[model].iloc[-1]*100))
                    emission_difference.append(abs(emissions_result[model].iloc[-1]-emissions_result2[model].iloc[-1])*1000)
                    performance_difference.append(abs(metrics_result[model].iloc[-1]-metrics_result2[model].iloc[-1]))
                plt.scatter(performance_difference, emission_difference)
                for i, txt in enumerate(models):
                    plt.annotate(txt, (performance_difference[i], emission_difference[i]))
                plt.xlabel('ABS Performance decrease ')
                plt.ylabel('log2 ABS Emission decrease (g)')
                #remove _confrontoEmissioni from dataset in datsaset_label
                dataset_label=dataset.replace('_40_7','')
                plt.title('Performance decrease vs Emission decrease '+dataset_label + ' ' + metric, fontsize=10)
                plt.yscale(matplotlib.scale.LogScale(base=2, axis='y'))
                plt.show()
                plt.grid(True)
                plt.gcf().set_size_inches(10, 5)
                plt.savefig(BASE_PATH + '/graphs2/decrement_'+metric+'_'+dataset+'.png')
                plt.close()
                del metrics_result, metrics, metrics_result2, metrics2



def sensibilityGraph():
    dataset_classic_criteria = ['movielens_1m_conEm']
    dataset_modified_criteria = [
        'movielens_1m_40_5', 'movielens_1m_30_5', 'movielens_1m_40_6',
        'movielens_1m_30_6', 'movielens_1m_40_7', 'movielens_1m_30_7'
    ]

    emissions_result = {}
    metrics_result = {}
    experiments_modified_list = []

    # Caricamento dei dati per il criterio classico
    for dataset in dataset_classic_criteria:
        for model in models:
            results_path = os.path.join(RESULT_PATH, dataset, model)
            metrics = pd.read_csv(os.path.join(results_path, "metrics.csv"))
            emissions = pd.read_csv(os.path.join(results_path, "emissions.csv"))
            metrics_result[model] = metrics
            emissions_result[model] = emissions

    # Caricamento dei dati per i criteri modificati
    for dataset in dataset_modified_criteria:
        metrics_result2 = {}
        emissions_result2 = {}
        for model in models:
            results_path = os.path.join(RESULT_PATH2, dataset, model)
            metrics = pd.read_csv(os.path.join(results_path, "metrics.csv"))
            emissions = pd.read_csv(os.path.join(results_path, "emissions.csv"))
            metrics_result2[model] = metrics
            emissions_result2[model] = emissions
        experiments_modified_list.append([metrics_result2, emissions_result2])

    # Plot delle curve di sensibilità
    for metric in metrics_list:
        for model in models:
            emission_difference = []
            performance_difference = []
            for i, experiment in enumerate(experiments_modified_list):
                emission_diff = abs(emissions_result[model].loc[0, 'emissions'] - experiment[1][model].loc[0, 'emissions']) * 1000
                performance_diff = abs(metrics_result[model][metric].iloc[-1] - experiment[0][model][metric].iloc[-1])
                emission_difference.append(emission_diff)
                performance_difference.append(performance_diff)
                plt.annotate(f"{model}-{dataset_modified_criteria[i]}", (emission_diff, performance_diff), fontsize=10, textcoords="offset points", xytext=(7, 7))
            
            plt.scatter(emission_difference, performance_difference, label=model)

        plt.xlabel('ABS Emission decrease')
        plt.ylabel('ABS Performance decrease')
        plt.title(f'Performance decrease vs Emission decrease - {metric}', fontsize=10)
        plt.gcf().set_size_inches(20, 10)
        #plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(BASE_PATH + '/graphs2/', f'sensibility2_{metric}.png'))
        plt.show()
        plt.close()




plot_emission()
#plot_metrics_comparison()
#print_table()
#printEmissionScorePlot()
#sensibilityGraph()




             

        

