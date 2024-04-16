# TIROCIINIO e TESI LAUREA TRIENNALEE IN INFORMATICA UniBa

Il lavoro è ereditato dalla seguente repository: [sustainability-of-recsys](https://github.com/albertovalerio/sustainability-of-recsys)


# sustainability-of-recsys
The system tracks the emissions of a given recommendation algorithm on a given dataset. It performs the model execution by applying the default parameters set or by applying the hyperparameters tuning carrying out the grid search. It also saves the metrics and the parameters configuration obtained during each run.

**Recommendations models, datasets and metrics refers to [@Recbole](https://recbole.io/) implementation.**

**Emission tracking is made by mean of [@CodeCarbon](https://mlco2.github.io/codecarbon/) library.**


## Requirements
* **Global requirements**: Python >= 3.7 (tested on 3.8.5 and 3.11.4)
* **System requirements**: see [requirements.txt](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/requirements.txt)


## Scripts

1. [**<ins>src/tuning_tracker.py</ins>**](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/src/tuning_tracker.py) performs the hyper-parameter tuning of a given algorithm on a given dataset (both passed as script’s arguments), carrying out the grid-search.

NOTES:
- All the available models and datasets are defined in [src/config/global_config.py](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/src/config/global_config.py) file.
- All the grid-search params ranges for each model are defined in [src/config/hyperparam](https://github.com/albertovalerio/sustainability-of-recsys/tree/main/src/config/hyperparam) folder.
- The results are saved in [results](https://github.com/albertovalerio/sustainability-of-recsys/tree/main/results) folder.
- Parameters names are case unsensitive while parameters values are case sensitive.

**Example**
```python
$ python3 src/tuning_tracker.py --dataset=mind --model=BPR
```
2. [**<ins>src/default_tracker.py</ins>**](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/src/default_tracker.py) tracks the emissions of a given algorithm with default and statically defined parameters on a given dataset (both passed as script’s arguments).

NOTES:
- All the available models and datasets are defined in [src/config/global_config.py](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/src/config/global_config.py) file.
- The deafult parameters are definded in [src/config/params_config.py](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/src/config/params_config.py) file.
- The results are saved in [results_shared](https://github.com/albertovalerio/sustainability-of-recsys/tree/main/results_shared) folder.
- Parameters names are case unsensitive while parameters values are case sensitive.

**Example**
```python
$ python3 src/default_tracker.py --dataset=mind --model=BPR
```
3. [**<ins>src/clear_cache.py</ins>**](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/src/clear_cache.py) the libraries and modules above mentioned automatically generate a series of intermediate results, serializations and logs, this script was created to remove them from file system, especially useful in the early stages of work.

It accepts the following arguments:

| Flag | Description |
|---|---|
|--log|It removes the contents of the **log** folder.|
|--tb|It removes the contents of the **log_tensorboard** folder.|
|--results|It removes the contents of the **results** and **results_shared** folders.|
|--saved|It removes the contents of the **saved** folder.|
|--all|It removes all the previous folders.|

**Example**
```python
$ python3 src/clear_cache.py --saved
```


## Notebooks
* [notebooks/tuning-results.ipynb](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/notebooks/tuning-results.ipynb) overview of the results obtained by performing the hyperparameter tuning on a selected subset of models and datasets.
* [notebooks/defaults-results.ipynb](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/notebooks/defaults-results.ipynb) overview of the results obtained by performing the same selected subset of models and datasets with defaults parameters.
* [notebooks/counters.ipynb](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/notebooks/counters.ipynb) overview of the execution times necessary to perform the experiments for each model involved. The total number of runs involved in the grid search for each model available is also shown.
* [notebooks/model-building.ipynb](https://github.com/albertovalerio/sustainability-of-recsys/blob/main/notebooks/model-building.ipynb) a proposal for a ML model able to predict the expected emissions for a given model and dataset represented by a set of features (**currently-under-development**).

## Datasets

* [data/amazon_books_60core_kg](https://github.com/albertovalerio/sustainability-of-recsys/tree/main/data/amazon_books_60core_kg): dataset about books. Knowledge data is also available.
* [data/mind](https://github.com/albertovalerio/sustainability-of-recsys/tree/main/data/mind): dataset about news. Knowledge data is not available.
* [data/movielens](https://github.com/albertovalerio/sustainability-of-recsys/tree/main/data/movielens): dataset about movies, version size 100K. Knowledge data is also available.
* [data/movielens_1m](https://github.com/albertovalerio/sustainability-of-recsys/tree/main/data/movielens_1m): dataset about movies, version size 1M. Knowledge data is also available.

## Results

Experiments were carried out for the hyperparameter tuning on the following resources:

* CPU: 1 x AMD EPYC 7V12.
* GPU: 1 x NVIDIA Tesla T4.
* RAM: 28 GB (plus 27 GB of swap space).

The selected models and datasets list is as follow:

* Datasets: **amazon_books_60core_kg**, **mind**, **movielens_1m**.
* Models: **BPR**, **CFKG**, **CKE**, **DMF**, **ItemKNN**, **KGNNLS**, **LINE**, **LightGCN**, **MultiDAE**, **SpectralCF**.

NOTE: since no external knowledge was available for the Mind datasets, knowledge-aware models (CFKG, CKE and KGNNLS) have not been trained on that dataset.

### amazon_books_60core_kg

![amazon results](/graphs/amazon_results.png)
![amazon tradeoff](/graphs/amazon_tradeoff.png)
![amazon power](/graphs/amazon_power.png)

### mind

![mind results](/graphs/mind_results.png)
![mind tradeoff](/graphs/mind_tradeoff.png)
![mind power](/graphs/mind_power.png)

### movielens_1m

![movielens results](/graphs/movielens_results.png)
![movielens tradeoff](/graphs/movielens_tradeoff.png)
![movielens power](/graphs/movielens_power.png)

**NOTE: <ins>for a more extensive analysis of results please refers to notebooks section</ins>.**

## Authors

The present project has been realized by me **[@albertovalerio](https://github.com/albertovalerio)** and my colleague **[@FranchiniFelice720034](https://github.com/FranchiniFelice720034)** as university laboratory activity for the exam in **Semantics In Intelligent Information Access**, Master's Degree in Computer Science, curriculum studies in Artificial Intelligence, with **Professor Giovanni Semeraro** and **Professor Cataldo Musto** and the supervision of PHD student **[@giuspillo](https://github.com/giuspillo)** at University of Bari "Aldo Moro", Italy.

## Acknowledgments

- **[@Recbole](https://recbole.io/)**
- **[@CodeCarbon](https://mlco2.github.io/codecarbon/)**

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See `LICENSE.txt` for more information.