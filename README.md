### 遺伝子の報告件数をCount値で算出する

<br>

NCBIのFTPサイトからgene2ensembl.gzとgene2pubmed.gzをダウンロードして解凍する。
https://ftp.ncbi.nlm.nih.gov/gene/DATA/

gene2ensembl.gzは、NCBIのgene IDとEnsemblのgene IDなどの対応表
gene2ensembl.gzを利用してEnsemblのgene IDをNCBIのgene IDに変換する

ファイルのパスや対象の生物種は以下の箇所を書き換えることで変更可能
生物種の選択はNCBIのTaxonomy IDで指定する
````
# settings
ensemblID_data_path = '../sus_scrofa_meta_analysis/5_score_results/hypoxia_code/CodingGene/score_geneid.csv'
gene2ensembl_data_path = './gene2ensembl.tsv'
gene2pubmed_data_path = './gene2pubmed.tsv'
tax_id = 9823
`````
<br>

pandasとpolarsでは、polarsの方が10倍ほど高速に処理できる。