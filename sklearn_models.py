import numpy as np
import pandas as pd
import pickle
import time
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
    trainningT0 = time.time()
    model.fit(Xtrain, Ytrain)
    trainningT1 = time.time()
    predictingT0 = time.time()
    predicted = model.predict(Xtest)
    predictingT1 = time.time()
    dtrainning = trainningT1-trainningT0
    dpredicting = predictingT1-predictingT0
    return model, predicted, dtrainning, dpredicting

def load_data():
    filename = "data/clean_tagged_features_unclean.csv"
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

def get_model_score(model,predicted, sets, filename, dtrainning, dpredicting):
    print("cross validating")
    Xtrain, Xtest, Ytrain, Ytest = sets
    validatingT0 = time.time()
    cv_scores = cross_val_score(model, Xtrain, Ytrain, cv=5)
    validatingT1 = time.time()
    dvalidate = validatingT1-validatingT0
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
        file.write(str(std)+"\n")
        file.write("time it took to train model: ")
        file.write(str(dtrainning)+"\n")
        file.write("time it took to predict: ")
        file.write(str(dpredicting)+"\n")
        file.write("time it took to cross-validate: ")
        file.write(str(dvalidate)+"\n")

if __name__ == "__main__":
    print("loading data")
    X, Y = load_data()
    print("splitting data into trainning and test data sets")
    sets = split_datasets(X,Y)
    print("trainning models")
    for i, classifier in enumerate(classifiers):
        print("trainning-testing model ",i,"/8 :",classifier_names[i])
        model, predicted, tt, tp = train_predict(sets, classifier)
        #see how model performed
        print("getting score for model ",i,"/8 :",classifier_names[i])
        get_model_score(model, predicted, sets, "results/all/"+classifier_names[i]+".txt", tt, tp)
