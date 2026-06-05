# Bringing Pragmatics to Porttinari - Adding Speech Acts to News Texts

This repository presents the corpus and codes presented by the paper "Bringing Pragmatics to Porttinari - Adding Speech Acts to News Texts".

## Repository structure
- data: Presents a subset of the Porttinari-base corpus manually annotated with Speech Acts
- results: Presents all .csv with results from executions of the Finetuning_BERTimbau_paper.ipynb notebook on the validation and test bases. These are the same results presented in the paper
- Finetuning_BERTimbau_paper.ipynb: notebook that performs BERTimbau finetuning

## Experiments

- Env: to run the experiments we used Google Colab with GPUs. You just need to upload your notebook to Google Colab to run it.
- Dependencies: considering the Google Colab environment, it is only necessary to install the transformer
-     pip install transformers

## Dataset


How to access the dataset:
- download csv file in 'data' folder
- upload the file to tools such as Excel, LibreOffice, Google Sheets


To access it in python:
-     df = pd.read_csv(r'data/porttinari-annotated-sample-paper-v1-20231211.csv')

## How to cite this work

    
    @inproceedings{speech-acts-porttinari,
        title = "Bringing Pragmatics to Porttinari - Adding Speech Acts to News Texts",
        author = "Nataly L. Patti Silva and Norton Trevisan Roman and Ariani Di Felippo",
        month = march,
        year = "2024"}
    

## More Details
Corpus Annotation Technical Report: [Report](http://ppgsi.each.usp.br/arquivos/RelTec/PPgSI-002_2023.pdf)
