import pandas as pd
import numpy as np
from os.path import dirname, abspath
from pipeline_utils import data_dir

def get_file_name(row):
    dirname = ""
    objid =""
    if row["Type"] == 1:
        dirname = data_dir +"raw/transients/"
        objid =str(row["ID"])
    elif row["Type"] == 0:
         dirname = data_dir +"raw/variables/"
         objid = str(int(row["ID"]))+".dat"
    return dirname, objid

def load_lc(dirname, filename):
    print(filename)
    time = ""
    lc = ""
    try: 
        if dirname.endswith("transients/"):
            data = pd.read_csv(dirname+filename, sep=",", names=["coords", "time", "mag", "error"], skiprows=1)
            time = pd.to_numeric(data["time"].str.split("(").str[0])
        
        elif dirname.endswith("variables/"):
            data = pd.read_csv(dirname+filename, sep=" ", names=["time", "mag", "error"])
            time = data["time"]

        mag = data['mag']
        error = data["error"]
        lc = np.array([np.asarray(mag.tolist()),np.asarray(time.tolist()),np.asarray(error.tolist())])
    except Exception as e:
        print('error: ',str(e))
    
    return lc
    

 

