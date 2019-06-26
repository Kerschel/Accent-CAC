# DEEP NEURAL NETWORKS FOR CARIBBEAN BASED ACCENT CLASSIFICATION
This repo contains the code,csv files for each experimental sets as well as a link to the data collection tool we created. The code include the files we used to preprocess our dataset,the CNN model we created from the accents as well as the code to train the neural network.The goal of this project was to create a accent classifer that is able to classify different Caribbean accents correctly. We used a 2D-CNN as our neural network and we had to collect data from Caribbean Countries ourselves since there were not many available resources we could use on recordings of Caribbean Accents.

## Table of Contents
1. [Data Collection tool](#datacollection)
2. [Dataset](#dataset)
3. [Code Explanation](#code)


## Data Collection tool
The code for our data collection system is available at https://github.com/Kerschel/Dataset-Speech-Collector
This code is hosted and can be accessed https://myaccent.app

## Dataset
The files for dataset can be accessed at [Experimental Datasets](https://myuwi-my.sharepoint.com/personal/kerschel_james_my_uwi_edu/Documents/Forms/All.aspx?cid=9dccd64e%2D9e0d%2D424b%2Dbce9%2D3b32d96af045&RootFolder=%2Fpersonal%2Fkerschel%5Fjames%5Fmy%5Fuwi%5Fedu%2FDocuments%2FShared%20with%20Everyone%2FExperimental%20Sets&FolderCTID=0x0120004A6371D9CFCA3D47BB05454C88E6E28E).

## CSV File Format
Each csv file is used to link the accent (HomeCountry) to a corresponding filename. We also added the duration of the file to be able to filter out the files that were not useful to us i.e persons who submitted very short recordings by error.
This filtering was done in [trainmodel.py](training/trainmodel.py) on line 154-161.

## Code Explanation
To run file use :
python trainmodel.py "experimental set csvfile" "modelname" "csvfilename for accuracy results"

* for example:
```bash
python trainmodel.py ES1.csv test_model output.csv
```
Note that depending on which Experimental set is used 

 The csv file to check the loss will be in the folder after running the code

* multiprocessing does not work with Jupyter, however the multiprocess is a stand in for multiprocessing
* https://pypi.org/project/multiprocess/