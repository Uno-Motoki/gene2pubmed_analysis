import matplotlib.pyplot as plt
import polars as pl
import numpy as np

# settings
ensemblID_data_path = '../sus_scrofa_meta_analysis/5_score_results/hypoxia_code/CodingGene/score_geneid.csv'
gene2ensembl_data_path = './gene2ensembl.tsv'
gene2pubmed_data_path = './gene2pubmed.tsv'
tax_id = 9823

# ----------convert Ensembl geneID to NCBI geneID----------

# Read the data
df = pl.read_csv(ensemblID_data_path, columns=['GeneID', 'HN1.5'])

# Read the gene2ensebml data
df_gene2ensembl = pl.read_csv(gene2ensembl_data_path, separator='\t')
df_gene2ensembl = (
	df_gene2ensembl
	.select(pl.col('#tax_id'), pl.col('GeneID'), pl.col('Ensembl_gene_identifier'))
	.filter(pl.col('#tax_id') == tax_id)
)
#print('df_gene2ensembl', df_gene2ensembl.head(10))

# Merge the data by ensembl gene ID
df_merged = (
	df
	.join(df_gene2ensembl, left_on='GeneID', right_on='Ensembl_gene_identifier', how='left')
	.rename({'GeneID': 'Ensembl_geneID'})
)
#print('df_merged', df_merged.head(10))

# Select sort rename the data
df_selected = (
	df_merged
	.sort(by='HN1.5', descending=True)
	.rename({'GeneID_right': 'NCBIGeneID'})
)
#print('df_selected', df_selected.head(10))

# ----------count how well gene has been studied----------

# Read the gene2pubmed data
df_gene2pubmed = pl.read_csv(gene2pubmed_data_path, separator='\t')
df_gene2pubmed_selected = df_gene2pubmed.filter(pl.col('#tax_id') == tax_id)
#print('gene2pubmed_selected', df_gene2pubmed_selected.head(10))

# Count how well gene has been studied and make the data table
df_counted_data = (
	df_gene2pubmed_selected
	.group_by('GeneID')
	.agg(pl.count('PubMed_ID').alias('Count'), pl.col('PubMed_ID').alias('Paper'))
)
#print('df_counted_data', df_counted_data.head(10))

# ----------merge the data----------
df_result_analysis = (
	df_selected
	.join(df_counted_data, left_on='NCBIGeneID', right_on='GeneID', how='left')
	.drop('#tax_id')
)

print('df_result_analysis', df_result_analysis.head(10))

# ----------plot the data----------
# plot the data
plt.scatter(df_result_analysis['HN1.5'], df_result_analysis['Count'])
plt.xlabel('HN1.5')
plt.ylabel('Count')
plt.title('Gene2pubmed analysis')

plt.axvline(x=0, color='red', linewidth=1, linestyle='--')

plt.show()