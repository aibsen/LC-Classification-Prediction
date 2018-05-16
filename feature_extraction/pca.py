from utils import clean_feature_list
from sklearn.decomposition import PCA
import pandas as pd
from os.path import dirname, abspath

if __name__ == "__main__":
  
    data_dir = dirname(dirname(abspath(__file__)))+"/data/"
    # output = data_dir+"pca/all-classes/pca"
    # inputFile = data_dir+"standard-features/all-classes/clean_tagged_features.csv"
    output = data_dir+"pca/main-classes/pca"
    inputFile = data_dir+"standard-features/main-classes/clean_tagged_features.csv"
    data = pd.read_csv(inputFile, sep=",")
    X = data[clean_feature_list]
    Y = data["tag"]
    
    for n in [5,10,15]:
        pca = PCA(n_components=n)
        new_X = pca.fit_transform(X)
        newdf = pd.DataFrame(new_X)
        newdf["tag"]=Y
        newdf.to_csv(output+str(n)+".csv", sep=',')
