# CarbonRecommenderRecSys23
Source code and datasets for the paper "Towards Sustainability-aware Recommender Systems: Analyzing the Trade-off Between Algorithms Performance and Carbon Footprint"

### Requirements
* RecBole 1.1.1: https://recbole.io/
* CodeCarbon: https://codecarbon.io/
* Pytorch

If you should need more info about the requirements, 'req.txt' is the output of the 'pip freeze' command for the conda environment used for these experiments.

### Python scripts

* 'script.py' launches the training for each dataset and for each model
* 'full_model.py' executes the training of the selected model on the selected dataset if no results have been computed for that setting, while keeping track of emissions during the training; then, it saves the results on a 'results' folder (which must be created).

## Datasets

* 'dataset/' contains the three datasets used for this experiment:
    * movielens 1m: dataset about movies, already splitted into train, validation, and test set. knowledge data is available for this dataset.
    * mind: dataset about news. to repliacate our experiments, set 'repeatable' to 'True' in the recbole parameter dict. no knowledge data is available for this dataset.
    * amazon books: dataset about books. to repliacate our experiments, set 'repeatable' to 'True' in the recbole parameter dict. knowledge data is available for this dataset.

RecBole 1.1.1 has been used: https://recbole.io/

CodeCarbon has been used:https://codecarbon.io/

Dataset have been preprocessed by us, and original version can be found here: https://github.com/RUCAIBox/RecSysDatasets


## Results

Graphical results obtained and described in the original paper.
Full results available in the 'results.xlsx' file.

### Mind
![](/graphs/sum_mind_dataset.png)
If the image should not be visible, it is possible to find it here: https://imgur.com/kzakVk2

### Movielens-1M
![](/graphs/sum_movielens_dataset.png)
If the image should not be visible, it is possible to find it here: https://imgur.com/4N2kY8F

### Amazon-books
![](/graphs/sum_amazon_books_dataset.png)
If the image should not be visible, it is possible to find it here: https://imgur.com/96Lh2zK


### Movielens-1M: Hyper-parameter impact

In this section, for some hyper-parameters (embedding size, negative examples), we set different values and compared with the default values. These experiments have been conducted on the ML1M dataset, considering DGCF as recommendation model, and considering two recommendation metrics (Recall@10, NDCG@10).
We considered these values:
* embedding size:
    * 32
    * 64 (default)
    * 128
* negative examples:
    * 1 (default)
    * 2

![](/graphs/sum_sens_movielens_dgcf.png)
If the image should not be visible, it is possible to find it here: https://imgur.com/bYjhqr5

Full results available in the 'sens.xlsx' file.


## Full results

* 'results.xlsx' is an Excel file containing all results measured and computed, including all metrics provided by CodeCarbon and all evaluation metrics provided by RecBole

* 'sens.xlsx' contains the full results of the hyper-parameter impact. 
