import pandas as pd
import numpy as np
from os.path import dirname, abspath


def load_lc(filename):
    print(filename)
    data = pd.read_csv(filename, sep=",", names=["coords", "time", "mag", "error"], skiprows=1)
    mag = data['mag']
    time = pd.to_numeric(data["time"].str.split("(").str[0])
    error = data["error"]
    lc = np.array([np.asarray(mag.tolist()),np.asarray(time.tolist()),np.asarray(error.tolist())])
    return lc

def get_file_name(row):
    filename = ""
    objid =""
    data_dir = dirname(dirname(abspath(__file__)))
    if row['Survey'] == 'CSS':
        objid = 'CSS'+str(row['images'])
        data_dir = data_dir+"/data0/"
    elif row['Survey'] == 'MLS':
        objid = 'MLS'+str(row['images'])
        data_dir = data_dir+"/data1/"
    elif row['Survey'] == 'SSS':
        objid = 'SSS'+str(row['images'])
        data_dir = data_dir+"/data2/"
    
    filename=data_dir+str(row['images'])
    return filename, objid
