# NaCTAR
We developed a natural product-derived drug discovery pipeline using data-driven approaches, named NaCTAR. 

We used Parkinson's disease as a case study to demonstrate the effectiveness of NaCTAR.

## Requirements
Python version
* `python` == 3.12


Require packages
* `pandas` == 2.2.3
* `seaborn` == 0.13.2
* `scipy` == 1.14.1
* `matplotlib` == 3.9.2


## Require input files
Input files need to run the codes. These files should be in the `data` folder.

* `pd_gene_compound_herb.tsv` - The relationships between compounds, herbs, and disease-related genes from COCONUT

* `pd_herb_phenotype.tsv` - The relationships between herbs and disease-related phenotypes from COCONUT

* `selected_herbs.tsv` - The list of herbs that are selected from the result of src/herb_compound_hit_count_visulization.py

* `pd_herb_compound_admet.tsv` - ADMET values for compounds (related to Parkinson's disease-related genes) in selected herbs from DrugBank

* `safe_compounds_from_TEST.tsv` - Compounds passed the TEST (toxicity test tool)

## Run analysis
Run `main.py`
