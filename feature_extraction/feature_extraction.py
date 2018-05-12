import numpy as np
import pandas as pd
import csv
import importlib
import feature_functions as f
from utils import feature_list
from load_lc import load_lc
from load_lc import get_file_name
import sys
from os.path import dirname, abspath

function_list = [getattr(f, x) for x in feature_list]
featuresdf = pd.DataFrame(columns=feature_list)
errorsdf = pd.DataFrame(columns=['filename','error'])

def get_features(lc,tag, objid):
    global featuresdf
    features = list(map(lambda f: f(lc), function_list))
    row = pd.DataFrame([features],columns=feature_list)
    row["id"] = objid
    row['tag'] = tag
    featuresdf = pd.concat([featuresdf, row],  ignore_index=True)

def clean(mag,time,error):
    m = np.mean(error)
    clean_date = []
    clean_mag = []
    clean_error = []	
    for i in range(len(mag)):
        if error[i] < (3 * m) and (np.absolute(mag[i] - np.mean(mag)) / np.std(mag)) < 5 :
            clean_date.append(time[i])
            clean_mag.append(mag[i])
            clean_error.append(error[i])
    clean_mag = np.asarray(clean_mag)	
    clean_date = np.asarray(clean_date)	
    clean_error = np.asarray(clean_error)	
    return [clean_mag, clean_date, clean_error]

if __name__ == "__main__":
    outputname = "tagged_features.csv"
    eoutputname = "errors_processing_features.csv"
    inputFilename = "tagged_meta_data.csv"

    if len(sys.argv)>1:
        inputFilename = sys.argv[1]+".csv"
    if len(sys.argv)>2:
        outputname = sys.argv[2]+".csv"
    if len(sys.argv)>3:
        eoutputname = sys.argv[3]+".csv"

    data_dir = dirname(dirname(abspath(__file__)))+"/data/"
    inputFile = data_dir+inputFilename
    fieldnames =  ["ID","RA (J2000)","Dec (J2000)","UT Date","Mag","images","SDSS",
        "Others","Followed","Last","LC","FC","Classification","SubClassification","Survey","tag"]
    tagged_metadata = pd.read_csv(inputFile, sep=",", names=fieldnames, skiprows=1)
    
    for index, row in tagged_metadata.iterrows():
        filename, objid = get_file_name(row)
        lc = load_lc(filename)
        tag = row['tag']
        try:
            print("Trying to get features for: ", filename)
            get_features(lc, tag, objid)
        except Exception as e:
            print('error: ',str(e))
            print("something went wrong when trying to process file: ", filename)
            error = {'filename':[filename],'error': [str(e)]}
            error_row = pd.DataFrame(data=error)
            errorsdf = pd.concat([errorsdf, error_row],ignore_index=True)
    #save features + errors
    featuresdf.to_csv(output, sep=',')
    errorsdf.to_csv(eoutput, sep=",")
    
    


