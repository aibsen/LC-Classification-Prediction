import csv
import pandas as pd
import numpy as np
from utils import feature_list


if __name__ == "__main__":
    #load tagged features
    # filename = "data/tagged_features.csv"
    filename = "data/tagged_features_unclean.csv"
    tagged_features = pd.read_csv(filename, sep=",")
    X = tagged_features[feature_list]
    #replace infinite values for nan, to take are of both
    X=X.replace([np.inf, -np.inf], np.nan)
    #see where nan values are
    where_are_nans = X.isnull()
    #group nan values by feature, to see what features are causing trouble
    sum_nans = where_are_nans.sum()
    feature_nans = list(sum_nans[sum_nans[feature_list]>0].keys())
    #for every feature that's giving nan values, drop the feature if 
    #too many values are nan, drop the object if it's an isolated case
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

    #remove classes Unknown/Other (6 and 8)
    tagged_features = tagged_features[(tagged_features['tag']!=6) & (tagged_features['tag']!=8)]
    print(tagged_features.shape)
    
    #save preprocessed features
    # tagged_features.to_csv("data/clean_tagged_features.csv", sep=',')
    tagged_features.to_csv("data/clean_tagged_features_unclean.csv", sep=',')