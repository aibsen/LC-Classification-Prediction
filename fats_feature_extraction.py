import numpy as np
import pandas as pd
import csv
import importlib
import feature_functions as f
from utils import feature_list
from load_lc import load_lc, get_file_name
import sys
from os.path import dirname, abspath
from pipeline_utils import unified_fieldnames, data_dir

function_list = [getattr(f, x) for x in feature_list]
featuresdf = pd.DataFrame(columns=feature_list)
errorsdf = pd.DataFrame(columns=['filename','error'])

def get_features(lc,tag1,tag2, objid):
    global featuresdf
    features = list(map(lambda f: f(lc), function_list))
    row = pd.DataFrame([features],columns=feature_list)
    row['ID'] = objid
    row['Type'] = tag1
    row['SubType'] = tag2
    featuresdf = pd.concat([featuresdf, row],  ignore_index=True)

def fats_feature_extraction(ffilename, errorfilename):
    global errorsdf
    global featuresdf
    # tagged_metadata = load_tagged_metadata(inputFilename)
    # lc_metadata = data_dir+"metadata/lc_metadata.csv"
    tagged_metadata = pd.read_pickle(data_dir+"metadata/lc_metadata.pkl")
    # tagged_metadata = pd.read_csv(lc_metadata,names=unified_fieldnames,skiprows = 1)
    # print(tagged_metadata)
    for index, row in tagged_metadata.iterrows():
        dirname, filename = get_file_name(row)
        lc = load_lc(dirname, filename)
        if lc != "":
            tag1 = row["Type"]
            tag2 = row["SubType"]
            objid = row["ID"]
            try:
                print("Trying to get features for: ", filename)
                get_features(lc, tag1,tag2, objid)
            except Exception as e:
                print('error: ',str(e))
                print("something went wrong when trying to process file: ", filename)
                error = {'filename':[filename],'error': [str(e)]}
                error_row = pd.DataFrame(data=error)
                errorsdf = pd.concat([errorsdf, error_row],ignore_index=True)
    # #save features + errors
    # data_dir = dirname(dirname(abspath(__file__)))+"/data/"
    featuresdf.to_pickle(ffilename)
    errorsdf.to_pickle(errorfilename)
    
    


