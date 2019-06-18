# Accent-CAC
To run file use :

python trainmodel.py short.csv "modelname" "csvfilename for accuracy results"

* for example:

```bash
python trainmodel.py short.csv test_model output.csv
```

 The csv file to check the loss will be in the folder after running the code

* multiprocessing does not work with Jupyter, however the multiprocess is a stand in for multiprocessing
* https://pypi.org/project/multiprocess/