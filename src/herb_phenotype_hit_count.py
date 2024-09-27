import pandas as pd

"""
20240805 shjung
Get scores of herbs
score: # of related phenotype of herbs
:return: herb score dataframe
"""

def main():
    phen_herb_df = pd.read_csv("../data/pd_herb_phenotype.tsv", sep='\t') # table 3
    phen_herb_df.drop_duplicates(inplace=True)
    herb_phen_hit_df = get_herb_phenotype_hit(phen_herb_df)
    herb_phen_hit_df.sort_values(by='phen_count', ascending=False, inplace=True)
    herb_phen_hit_df.to_csv("../result/pd_herb_phenotype_hit_count.tsv", sep='\t') # table 4
    return 0


def get_herb_phenotype_hit(phen_herb_df):
    df = phen_herb_df
    herb_list = list(df['herb_name'].unique())
    result = pd.DataFrame(index=herb_list, columns=['phen_count'])
    for herb in herb_list:
        herb_df = search_by_herb(df, herb)
        herb_phenotype_hit = len(herb_df)
        result.loc[herb] = herb_phenotype_hit

    result.index.name = 'herb_name'
    return result

def search_by_herb(df, herb):
    result = df.loc[df['herb_name'] == herb]
    return result


if __name__ == "__main__":
    main()