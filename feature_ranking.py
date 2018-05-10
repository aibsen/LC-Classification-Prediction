from sklearn.decomposition import PCA
from utils import clean_feature_list
import pandas as pd
import numpy as np

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import GenericUnivariateSelect
from sklearn.decomposition import PCA


feature_selection_methods = [
    VarianceThreshold(threshold=(.8 * (1 - .8))),
    SelectKBest(k=5),
    SelectKBest(score_func=mutual_info_classif, k=5),
    SelectPercentile(percentile = 25),
    GenericUnivariateSelect(),
    GenericUnivariateSelect(score_func=mutual_info_classif),
    # RFE(estimator, n_features_to_select=5),
] 

feature_selection_names = [
    "VarianceThreshold 80%",
    "SelectKBest(k=5)",
    "SelectKBest(mutual_info_classif, k=5)",
    "SelectPercentile 25",
    "GenericUnivariateSelect",
    "GenericUnivariateSelect(mutual_info_classif)",
    # RFE(estimator, n_features_to_select=5),
]  

if __name__ == "__main__":
    inputFile = "data/clean_tagged_features.csv"
    data = pd.read_csv(inputFile, sep=",")
    X = data[clean_feature_list]
    Y = data["tag"]
    for i,selection in enumerate(feature_selection_methods):
        fit = selection.fit(X,Y)
        features = selection.get_support(indices=True)
        feature_names = [clean_feature_list[item] for item in features]        
        print(feature_selection_names[i]+": "+ str(feature_names))
