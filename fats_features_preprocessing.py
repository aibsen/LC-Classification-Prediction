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
    feature_nans = list(sum_nans[sum_nans[feature_list]>0].keys())
    # feature_nans = list(sum_nans[sum_nans[dmdtnames]>0].keys())
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
    tagged_features = tagged_features[~((tagged_features['SubType']==5) & (tagged_features['Type']==1))]
    return tagged_features

def fats_features_preprocessing(outputFile,inputFile):
    print("input   ", inputFile)
    tagged_features = pd.read_pickle(inputFile)
    print("shape before pre_processing: ",tagged_features.shape)
    X = tagged_features[feature_list]
    # X=tagged_features[dmdtnames]
    tagged_features = remove_nan_inf(X, tagged_features)
    tagged_features = remove_unkown_others(tagged_features)   
    print("shape after pre_processing: ",tagged_features.shape)
    tagged_features.to_pickle(outputFile)