import pandas as pd
import numpy as np
from os.path import dirname, abspath

main_dir = dirname(dirname(abspath(__file__)))

def load_tagged_metadata(inputFilename):
    data_dir = main_dir+"/data/"
    inputFile = data_dir+inputFilename
    fieldnames =  ["ID","RA (J2000)","Dec (J2000)","UT Date","Mag","images","SDSS",
        "Others","Followed","Last","LC","FC","Classification","SubClassification","Survey","tag"]
    tagged_metadata = pd.read_csv(inputFile, sep=",", names=fieldnames, skiprows=1)
    return tagged_metadata

def load_lc(filename):
    data = pd.read_csv(filename, sep=",", names=["coords", "time", "mag", "error"], skiprows=1)
    mag = data['mag']
    time = pd.to_numeric(data["time"].str.split("(").str[0])
    error = data["error"]
    lc = np.array([np.asarray(mag.tolist()),np.asarray(time.tolist()),np.asarray(error.tolist())])
    return lc

def get_file_name(row):
    filename = ""
    objid =""
    if row['Survey'] == 'CSS':
        objid = 'CSS'+str(row['images'])
        data_dir = main_dir+"/data0/"
    elif row['Survey'] == 'MLS':
        objid = 'MLS'+str(row['images'])
        data_dir = main_dir+"/data1/"
    elif row['Survey'] == 'SSS':
        objid = 'SSS'+str(row['images'])
        data_dir = main_dir+"/data2/"
    
    filename=data_dir+str(row['images'])
    return filename, objid
