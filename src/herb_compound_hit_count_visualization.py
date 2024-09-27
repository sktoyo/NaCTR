import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
"""
20240805 shjung
Draw scores of herbs
score1: # of compound targeting therapeutic genes among herbs 
score2: # of related phenotype of herbs
:return: scatter plot
"""

def main():
    herb_compound_hit_df = pd.read_csv("../result/pd_herb_compound_hit_count.tsv", sep='\t', index_col=0)

    herb_phenotype_hit_df = pd.read_csv("../result/pd_herb_phenotype_hit_count.tsv", sep='\t', index_col=0)

    draw_herb_comp_hist(herb_compound_hit_df)
    draw_herb_phen_hist(herb_phenotype_hit_df)

    herb_df = pd.merge(herb_compound_hit_df, herb_phenotype_hit_df, left_index=True, right_index=True)
    herb_df.to_csv("../result/pd_herb_count_selection.tsv", sep='\t')
    herb_df = herb_df[['comp_count', 'phen_count']]
    draw_scatter_plot(herb_df)



def draw_herb_comp_hist(herb_compound_hit_df):
    df = herb_compound_hit_df
    sns.set(style="whitegrid")

    plt.figure(figsize=(8, 6))
    sns.histplot(df['comp_count'], kde=False)
    plt.title('Distribution of herb_compound score')
    plt.xlabel('Herb score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


def draw_herb_phen_hist(herb_phenotype_hit_df):
    df = herb_phenotype_hit_df
    sns.set(style="whitegrid")

    plt.figure(figsize=(8, 6))
    sns.histplot(df['phen_count'], kde=False)
    plt.title('Distribution of herb_phenotype score')
    plt.xlabel('Herb score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


def draw_scatter_plot(herb_df):
    corr, p_value = spearmanr(herb_df['comp_count'], herb_df['phen_count'])
    print('Spearman correlation: {:.2f}, p-value: {:.4f}'.format(corr, p_value))
    grouped = herb_df.groupby(['comp_count', 'phen_count']).size().reset_index(name='counts')
    sns.set(style="whitegrid")

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='comp_count', y='phen_count', size='counts', sizes=(50, 500), data=grouped, alpha=0.6, legend=False)
    sns.regplot(x='comp_count', y='phen_count', data=herb_df, scatter=False, color='red', line_kws={"label": f"Spearmanr={corr:.2f}"})

    plt.title('Scatter plot of Herb compound hit and phenotype hit count')
    plt.xlabel('Hit compound count')
    plt.ylabel('Hit phenotype count')
    plt.grid(True)
    plt.show()


if '__main__' == __name__:
    main()