import numpy as np
import pandas as pd
import pickle
from utils import clean_feature_list

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

classifiers = [
    KNeighborsClassifier(),
    SVC(),
    GaussianProcessClassifier(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    MLPClassifier(),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]

classifier_names = ["Nearest Neighbors", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]

def train_predict(sets, model):
    Xtrain, Xtest, Ytrain, Ytest = sets
    print("training SVM")
    model.fit(Xtrain, Ytrain)
    print("testing SVM")
    predicted = model.predict(Xtest)
    return model, predicted

def train_SVM(sets):
    model = SVC()
    Xtrain, Xtest, Ytrain, Ytest = sets
    print("training SVM")
    model.fit(Xtrain, Ytrain)
    print("testing SVM")
    predicted = model.predict(Xtest)
    return model, predicted

def load_data():
    filename = "data/clean_tagged_features_unclean.csv"
    # filename = "data/clean_tagged_features.csv"  
    #reading data from csv
    data = pd.read_csv(filename, sep=",")
    X = data[clean_feature_list]
    Y = data["tag"] 
    return X,Y

def split_datasets(X,Y):
    #converting data to numpy arrays, so we can split dataset
    Xnp = X.as_matrix()
    Ynp = Y.as_matrix()
    X_train, X_test, Y_train, Y_test = train_test_split(Xnp, Ynp, test_size=0.3)
    size_of_trainning = X_train.shape
    size_of_test = X_test.shape
    print("size of trainning data set:",size_of_trainning[0])
    print("size of test data set:",size_of_test[0])
    return [X_train, X_test, Y_train, Y_test]

def get_model_score(model,predicted, sets, filename):
    print("cross validating")
    Xtrain, Xtest, Ytrain, Ytest = sets
    cv_scores = cross_val_score(model, Xtrain, Ytrain, cv=5)
    with open(filename,"w") as file:
        report = metrics.classification_report(Ytest, predicted)
        mean_score = np.mean(cv_scores)
        std = np.std(cv_scores)
        score = model.score(Xtest, Ytest)
        file.write("report: ")
        file.write(report)
        file.write("mean_score: ")
        file.write(str(mean_score)+"\n")
        file.write("std: ")
        file.write(str(std))

if __name__ == "__main__":
    print("loading data")
    X, Y = load_data()
    print("splitting data into trainning and test data sets")
    sets = split_datasets(X,Y)
    print("trainning models")
    model, predicted = train_SVM(sets)
    #see how model performed
    get_model_score(model, predicted, sets, "testnotclean.txt")

