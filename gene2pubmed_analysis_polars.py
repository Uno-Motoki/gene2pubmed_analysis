import matplotlib.pyplot as plt
import polars as pl
import numpy as np
from adjustText import adjust_text # install with pip install adjustText

# settings
ensemblID_data_path = '../gallus_gallus_analysis/5_score_result/chicken_score_geneID.csv'
geneID2geneSymbol_data_path = './chicken_geneId2geneSym.txt'
gene2ensembl_data_path = './gene2ensembl.tsv'
gene2pubmed_data_path = './gene2pubmed.tsv'
tax_id = 9031 # 9823: pig, 9031: chicken

# ----------convert Ensembl geneID to NCBI geneID----------

# Read the data
df = pl.read_csv(ensemblID_data_path, columns=['GeneID', 'HN1.5'])

#print('df', df.head(10))

df_geneID2geneSymbol = pl.read_csv(geneID2geneSymbol_data_path, separator='\t')

#print('df_geneID2geneSymbol', df_geneID2geneSymbol.head(10))

# Read the gene2ensebml data
df_gene2ensembl = pl.read_csv(gene2ensembl_data_path, separator='\t')
df_gene2ensembl = (
	df_gene2ensembl
	.select(pl.col('#tax_id'), pl.col('GeneID'), pl.col('Ensembl_gene_identifier'))
	.filter(pl.col('#tax_id') == tax_id)
)

# Merge the data by ensembl gene ID
df_merged = (
	df
	.join(df_gene2ensembl, left_on='GeneID', right_on='Ensembl_gene_identifier', how='left')
	.rename({'GeneID': 'Ensembl_geneID'})
)

#print('df_merged', df_merged.head(10))

df_merged = (
	df_merged
	.join(df_geneID2geneSymbol, left_on='Ensembl_geneID', right_on='Gene_stable_ID', how='left')
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
    .unique(subset=['Ensembl_geneID'], maintain_order=True)
)

#print('df_result_analysis', df_result_analysis.head(10))





# ----------plot the data----------
# plot the data

# add gene symbol
df_filtered = df_result_analysis.with_columns(
    pl.when(pl.col("Gene_name").is_null())
    .then(pl.col("Ensembl_geneID"))
    .otherwise(pl.col("Gene_name"))
    .alias("label")
)
print('df_filtered', df_filtered.head(10))

df_filtered = df_filtered.with_columns(
    pl.col('Count').fill_null(0),
)

print('df_filtered', df_filtered.head(10))

# 散布図をプロット
plt.scatter(df_filtered['HN1.5'], df_filtered['Count'])
plt.xlabel('HN1.5')
plt.ylabel('Count')
plt.title('Gene2pubmed analysis \n Chicken VS Red Junglefowl')
plt.axvline(x=0, color='red', linewidth=1, linestyle='--')

# 上位20件と下位20件を取得
top_20 = df_filtered.sort(by='HN1.5', descending=True).head(20)
bottom_20 = df_filtered.sort(by='HN1.5', descending=False).head(20)

# ラベルを追加
texts = []
for df in [top_20, bottom_20]:
    for label, x, y in zip(df['label'], df['HN1.5'], df['Count']):
        texts.append(plt.text(x, y, label))

# ラベルが重ならないように調整
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))

#plt.show()

# save the data

#df_filtered.drop('Paper','label').write_csv('./Chicken_gene2pubmed_analysis.csv', separator=',')
print('df_filtered', df_result_analysis.head(10))