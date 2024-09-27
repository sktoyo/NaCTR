import pandas as pd

"""
20240805 shjung
Get scores of herbs
score: # of compound targeting therapeutic genes among herbs 
"""


def main():
    gene_comp_herb_df = pd.read_csv("../data/pd_gene_compound_herb.tsv", sep='\t') # table 1
    gene_comp_herb_df = gene_comp_herb_df[['compound', 'herb_name']]
    gene_comp_herb_df = gene_comp_herb_df.drop_duplicates()

    herb_compound_hit_df = count_comp(gene_comp_herb_df)
    herb_compound_hit_df.to_csv("../result/pd_herb_compound_hit_count.tsv", sep='\t') # table 2
    return herb_compound_hit_df


def count_comp(gene_comp_herb_df):
    df = gene_comp_herb_df
    herb_list = list(df['herb_name'].unique())
    result = pd.DataFrame(index=herb_list, columns=['comp_count'])
    for herb in herb_list:
        herb_df = search_by_herb(df, herb)
        herb_phenotype_hit = len(herb_df)
        result.loc[herb] = herb_phenotype_hit

    result.index.name = 'herb_name'
    return result

def search_by_herb(df, herb):
    result = df.loc[df['herb_name'] == herb]
    return result


if '__main__' == __name__:
    herb_compound_hit_df = main()
