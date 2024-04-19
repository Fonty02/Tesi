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

models = ['ItemKNN','BPR', 'CFKG', 'CKE', 'DMF', 'KGCN', 'KGNNLS', 'LINE', 'MultiDAE', 'LightGCN']
datasets = ['ml-10m_50U10I']
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
        plt.title(dataset)
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
        plt.savefig(BASE_PATH + '/graphs/emissions_'+dataset+'.png')
        plt.close()
        del emissions_result, emissions


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
                plt.title(dataset)
                plt.ylabel(metric)
                plt.xlabel("Emissions log2")
                for i, model in enumerate(models):
                    plt.plot(emissions_result[model], metrics_result[model], 'o', label=model, color='blue')
                    plt.annotate(model, (emissions_result[model], metrics_result[model]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)
                plt.xscale(matplotlib.scale.LogScale(base=2,axis='x'))
                plt.grid(True)
                plt.show()
                plt.savefig(BASE_PATH + '/graphs/'+metric+'_'+dataset+'.png')
                plt.close()
                del metrics_result, metrics

plot_emission()
plot_metrics()




             

        

