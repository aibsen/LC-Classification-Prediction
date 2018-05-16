import csv
import pandas as pd
import numpy as np
from utils import feature_list
from utils import dmdtnames
import sys
from os.path import dirname, abspath

def remove_nan_inf(X, tagged_features):
    X=X.replace([np.inf, -np.inf], np.nan)
    where_are_nans = X.isnull()
    sum_nans = where_are_nans.sum()
    # feature_nans = list(sum_nans[sum_nans[feature_list]>0].keys())
    feature_nans = list(sum_nans[sum_nans[dmdtnames]>0].keys())
    arbitrary = 10
    for fnan in feature_nans:
        ids_nan = list(where_are_nans[where_are_nans[fnan]==True].index)      
        try:
            if len(ids_nan) > arbitrary:
                tagged_features = tagged_features.drop([fnan],axis=1)
            else:
                tagged_features = tagged_features.drop(ids_nan)
        except Exception as e:
            print('error: ',str(e))
            print('probably trying to drop value that has already been dropped')
    
    return tagged_features

def remove_unkown_others(tagged_features):    
    tagged_features = tagged_features[(tagged_features['tag']!=6) & (tagged_features['tag']!=8)]
    return tagged_features

def remove_hpm(tagged_features):
    tagged_features = tagged_features[tagged_features['tag']!=4]
    return tagged_features


if __name__ == "__main__":
  
    data_dir = dirname(dirname(abspath(__file__)))+"/data/"
    output = data_dir+"standard-features/all-classes/clean_tagged_features.csv"
    inputFile = data_dir+"standard-features/all-classes/tagged_features.csv"

    if len(sys.argv)>1:
        inputFile = data_dir+sys.argv[1]+".csv"
    if len(sys.argv)>2:
        output = data_dir+sys.argv[2]+".csv"
  
    print("input   ", inputFile)
    tagged_features = pd.read_csv(inputFile, sep=",")
    print("shape before pre_processing: ",tagged_features.shape)
    # X = tagged_features[feature_list]
    X=tagged_features[dmdtnames]
    tagged_features = remove_nan_inf(X, tagged_features)
    tagged_features = remove_unkown_others(tagged_features)   
    tagged_features = remove_hpm(tagged_features)    
    print("shape after pre_processing: ",tagged_features.shape)
    tagged_features.to_csv(output, sep=',')