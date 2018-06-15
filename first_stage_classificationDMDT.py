import numpy as np
import pandas as pd
import pickle
import time
import sys

from pipeline_utils import fnames0, fnames1

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

classifiers = [
    KNeighborsClassifier(),
    SVC(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    MLPClassifier(),
    AdaBoostClassifier(),
    GaussianNB(),
    ]

classifier_names = ["Nearest Neighbors", "RBF SVM", 
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes"]


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

def load_data(filename,fname):
    #reading data from pkl
    data = pd.read_pickle(filename)
    X = data[fname]
    Y = data["Type"] 
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

def get_model_score(name,model,predicted, sets, filename, dtrainning, dpredicting, index):
    print("cross validating")
    Xtrain, Xtest, Ytrain, Ytest = sets
    validatingT0 = time.time()
    cv_scores = cross_val_score(model, Xtrain, Ytrain, cv=5)
    validatingT1 = time.time()
    dvalidate = validatingT1-validatingT0
    with open(filename,"a") as file:
        report = metrics.classification_report(Ytest, predicted)
        mean_score = np.mean(cv_scores)
        std = np.std(cv_scores)
        score = model.score(Xtest, Ytest)
        file.write("dmdt"+str(index))
        file.write("report for "+name+" : ")
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
        file.write("\n")
        file.write("\n")

def first_stage_classificationDMDT(inputFile, outputFile):
    inputFile0 = inputFile+"0.pkl"
    inputFile1 = inputFile+"1.pkl"
    X0, Y0 = load_data(inputFile0,fnames0)
    X1, Y1 = load_data(inputFile1,fnames1)
    Y0 = Y0.astype("int")
    Y1 = Y1.astype("int")
    sets0 = split_datasets(X0,Y0)
    sets1 = split_datasets(X1,Y1)
    print("trainning models")
    for index,sets in enumerate([sets0,sets1]):
        for i, classifier in enumerate(classifiers):
            print("trainning-testing model ",i," :",classifier_names[i])
            model, predicted, tt, tp = train_predict(sets, classifier)
            #see how model performed
            print("getting score for model ",i," :",classifier_names[i])
            get_model_score(classifier_names[i],model, predicted, sets,outputFile, tt, tp, index)
    
    