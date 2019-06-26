#DEEP NEURAL NETWORKS FOR CARIBBEAN BASED ACCENT CLASSIFICATION
This repo contains the code,csv files for each experimental sets as well as a link to the data collection tool we created.

https://github.com/Kerschel/Dataset-Speech-Collector


The files for dataset can be accessed at [Experimental Datasets](https://myuwi-my.sharepoint.com/personal/kerschel_james_my_uwi_edu/Documents/Forms/All.aspx?cid=9dccd64e%2D9e0d%2D424b%2Dbce9%2D3b32d96af045&RootFolder=%2Fpersonal%2Fkerschel%5Fjames%5Fmy%5Fuwi%5Fedu%2FDocuments%2FShared%20with%20Everyone%2FExperimental%20Sets&FolderCTID=0x0120004A6371D9CFCA3D47BB05454C88E6E28E).


To run file use :

python trainmodel.py short.csv "modelname" "csvfilename for accuracy results"

* for example:

```bash
python trainmodel.py short.csv test_model output.csv
```

 The csv file to check the loss will be in the folder after running the code

* multiprocessing does not work with Jupyter, however the multiprocess is a stand in for multiprocessing
* https://pypi.org/project/multiprocess/