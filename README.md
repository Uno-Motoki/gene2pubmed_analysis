## 遺伝子の報告件数をCount値で算出する

<br>

### 必要なファイル
1. NCBIのFTPサイトから**gene2ensembl.gz**と**gene2pubmed.gz**をダウンロードして解凍する<br>
   gene2ensembl.gzは、NCBIのgene IDとEnsemblのgene IDなどの対応表で、EnsemblGeneIDをNCBIGeneIDに変換する際に利用する<br>
   https://ftp.ncbi.nlm.nih.gov/gene/DATA/
2. BioMartなどを利用して、GeneIDとGeneSymbolの対応表を作成する<br>

### Pathの設定
ファイルのパスや、対象の生物種は以下の箇所を書き換えることで変更可能<br>
生物種の選択はNCBIのTaxonomy IDで指定する
````
# settings
ensemblID_data_path = '../sus_scrofa_meta_analysis/5_score_results/hypoxia_code/CodingGene/score_geneid.csv'
gene2ensembl_data_path = './gene2ensembl.tsv'
gene2pubmed_data_path = './gene2pubmed.tsv'
tax_id = 9823
`````
<br>

>[!NOTE]
>pandasとpolarsでは、polarsの方が10倍ほど高速に処理できる
