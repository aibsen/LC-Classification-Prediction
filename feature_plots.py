import numpy as np
import pandas as pd
import seaborn as sns
# import matplotlib.pyplot as plt
from utils import clean_feature_list
import sys
from utils import ranked

#plots for all classes
def plot_all_classes(tagged_features, outputFile):
    fplot = sns.pairplot(tagged_features, hue="tag", vars=ranked, dropna=True)
    fplot.savefig(outputFile+".png")

#plots for each pair of classes
def plot_pairs_of_classes(tagged_features, outputFile):
    tags = [0,1,2,3,5,7]
    for i in tags:
        for j in tags:
            if j > i:
                items = tagged_features[(tagged_features.tag==i) | (tagged_features.tag ==j)]
                fplot = sns.pairplot(items, hue="tag", vars=clean_feature_list, dropna=True)
                fplot.savefig(outputFile+"_"+str(i)+"_"+str(j)+".png")

if __name__ == "__main__":
    inputFile = "data/clean_tagged_features.csv"
    outputFile = "results/feature_plots/feature_plots"
    outputFile2 = "results/feature_plots/feature_plots_classes"

    if len(sys.argv)>1:
        inputFile = "data/"+sys.argv[1]+".csv"
    if len(sys.argv)>2:
        outputFile = "results/"+sys.argv[2]
    if len(sys.argv)>3:
        outputFile2 = "results/"+sys.argv[3]

    tagged_features = pd.read_csv(inputFile, sep=",")

    plot_all_classes(tagged_features, outputFile)
    plot_pairs_of_classes(tagged_features, outputFile)