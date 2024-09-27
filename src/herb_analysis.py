import pandas as pd

"""
after the selection of herbs 
after herb_compound_hit_count_visualization.py
after TEST (toxicity test tool, ../data/safe_compounds_from_TEST.tsv)
selected herbs(../data/selected_herbs.csv):
Camellia sinensis
Theobroma cacao
Solanum lycopersicum
Solanum tuberosum
Zea mays
Carica papaya
Prunus persica 
"""


def main():
    herb_comp_compact_df, herb_phen_compact_df = get_herb_related_info()
    qualified_compounds = get_qualified_compounds()
    herb_qualified_comp_df = herb_comp_compact_df[herb_comp_compact_df['compound'].isin(qualified_compounds)]

    herb_qualified_comp_df.to_csv("../result/pd_herb_qualified_compounds.tsv", sep='\t', index=False) # table 7
    herb_phen_compact_df.to_csv("../result/pd_herb_selected_phenotype_compact.tsv", sep='\t', index=False) # table 8

    comp_count_df = herb_qualified_comp_df.groupby('herb_name').count()
    phen_count_df = herb_phen_compact_df.groupby('herb_name').count()

    count_df = pd.merge(comp_count_df, phen_count_df, left_index=True, right_index=True)
    count_df['count'] = count_df['compound'] + count_df['phen_name']
    count_df.columns = ['comp_count', 'phen_count', 'total_count']
    count_df.sort_values(by='total_count', ascending=False, inplace=True)
    count_df.to_csv('../result/pd_herb_final_count.tsv', sep='\t') # count of phenotypes and qualifed compounds

    qualified_compounds_target_df = get_target_gene(qualified_compounds)
    qualified_compounds_target_df.to_csv("../result/pd_qualified_compound_gene.tsv", sep='\t', index=False) # table 9


def get_herb_related_info():
    gene_comp_herb_df = pd.read_csv("../data/pd_gene_compound_herb.tsv", sep='\t')
    herb_phen_df = pd.read_csv("../data/pd_herb_phenotype.tsv", sep='\t')

    herb_list = pd.read_csv('../data/selected_herbs.tsv', sep ='\t', header=None)
    herb_list = herb_list.iloc[:, 0].to_list()

    filtered_herb_comp_df = pd.DataFrame()
    filtered_herb_phen_df = pd.DataFrame()
    for herb in herb_list:
        filtered_herb_comp_df = pd.concat([filtered_herb_comp_df, search_by_herb(gene_comp_herb_df, herb)])
        filtered_herb_phen_df = pd.concat([filtered_herb_phen_df, search_by_herb(herb_phen_df, herb)])

    herb_comp_compact_df = filtered_herb_comp_df[['herb_name', 'compound']].drop_duplicates()
    herb_phen_compact_df = filtered_herb_phen_df[['herb_name', 'phen_name']].drop_duplicates()
    return herb_comp_compact_df, herb_phen_compact_df


def search_by_herb(df, herb):
    result = df.loc[df['herb_name'] == herb]
    return result


def get_qualified_compounds():
    """
    Run this function after curating drugbank IDs and SMILES of compounds
    :return:
    """
    compound_admet = pd.read_csv('../data/pd_herb_compound_admet.tsv', sep='\t')
    compounds_passing_BBB = compound_admet[compound_admet['ADMET - Blood Brain Barrier_value'] == True].compound.to_list()
    """
    The below compounds from TEST, a toxicity prediction tool, result.
    If adapt it to other disease and herbs, you need new list
    """
    safe_compounds = pd.read_csv("../data/safe_compounds_from_TEST.tsv", sep='\t', header=None)
    safe_compounds = safe_compounds.iloc[:, 0].to_list()
    all_passing_compounds = list(set(compounds_passing_BBB) & set(safe_compounds))
    return all_passing_compounds


def check_herb_compound_hit(herb_comp_df):
    check_df = pd.DataFrame(index=herb_comp_df['herb_name'].unique(),
                            columns=herb_comp_df['compound'].unique())
    for row in herb_comp_df.iterrows():
        herb = row[1]['herb_name']
        comp = row[1]['compound']
        check_df.loc[herb, comp] = 1
    with pd.option_context('future.no_silent_downcasting', True):
        check_df.fillna(0, inplace=True)
    return check_df


def get_target_gene(qualified_compounds):
    gene_comp_herb_df = pd.read_csv("../data/pd_gene_compound_herb.tsv", sep='\t')
    filtered_df = gene_comp_herb_df[gene_comp_herb_df['compound'].isin(qualified_compounds)]
    filtered_df = filtered_df[['symbol', 'compound']].drop_duplicates()
    return filtered_df


if __name__ == "__main__":
    main()