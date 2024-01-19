#import matplotlib.pyplot as plt # can't use matplotlib install by conda. So, I installed matplotlib by pip.
import pandas as pd
import numpy as np


# settings
ensemblID_data_path = '../sus_scrofa_meta_analysis/5_score_results/hypoxia_code/CodingGene/score_geneid.csv'
gene2ensembl_data_path = './gene2ensembl.tsv'
gene2pubmed_data_path = './gene2pubmed.tsv'
tax_id = 9823

# ----------convert Ensembl geneID to NCBI geneID----------

# Read the data
df = pd.read_csv(ensemblID_data_path, usecols=['GeneID', 'HN1.5'])

# Read the gene2ensebml data
df_gene2ensembl = pd.read_csv(gene2ensembl_data_path, sep='\t', usecols=['#tax_id', 'GeneID', 'Ensembl_gene_identifier'])
df_gene2ensembl = df_gene2ensembl[df_gene2ensembl['#tax_id'] == tax_id]

# Merge the data by ensembl gene ID
df_merged = df.merge(df_gene2ensembl, left_on='GeneID', right_on='Ensembl_gene_identifier', how='left')
df_merged['GeneID_y'] = df_merged['GeneID_y'].fillna(pd.NA).astype('Int64')

# Select the data
df_selected_tmp = df_merged[['GeneID_y', 'HN1.5', 'GeneID_x']]
df_selected_tmp = df_selected_tmp.sort_values(by='HN1.5', ascending=False)
df_selected = df_selected_tmp.rename(columns={'GeneID_y': 'NCBIGeneID'})
#print(df_selected.head(10))

# ----------count how well gene has been studied----------

# Read the gene2pubmed data
df_gene2pubmed = pd.read_csv(gene2pubmed_data_path, sep='\t')
df_gene2pubmed_selected = df_gene2pubmed[df_gene2pubmed['#tax_id'] == tax_id]

# Count how well gene has been studied and make the data table
df_counted_data = (
    df_gene2pubmed_selected.groupby('GeneID')
    .agg(Count=('GeneID', 'size'), Paper=('PubMed_ID', lambda x: ','.join(x.astype(str))))
    .reset_index()
	.fillna(pd.NA) # convert NaN to NA
    .astype({'GeneID': 'Int64', 'Count': 'Int64', 'Paper': 'string'})
)
#print(df_counted_data.head(10))

# ----------merge the data----------
df_result_analysis = (
	df_selected.merge(df_counted_data, left_on='NCBIGeneID', right_on='GeneID', how='left')
	.rename(columns={'GeneID_x': 'Ensembl_geneID'})
	.drop(columns=['GeneID'])
)
print(df_result_analysis.head(10))