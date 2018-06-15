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
    transients = data[data["Type"]==1]
    Xt = transients[fname]
    Yt = transients["SubType"] 

    variables = data[data["Type"]==0]
    Xv = variables[fname]
    Yv = variables["SubType"] 
   
    return Xt,Yt,Xv,Yv

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

def get_model_score(type,name,model,predicted, sets, filename, dtrainning, dpredicting):
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
        file.write(type)
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

def second_stage_classificationDMDT(inputFile, outputFile):
    inputFile0 = inputFile+"0.pkl"
    inputFile1 = inputFile+"1.pkl"
    Xt0, Yt0, Xv0, Yv0 = load_data(inputFile0,fnames0)
    Yt0 = Yt0.astype("int")
    Yv0 = Yv0.astype("int")
    Xt1, Yt1, Xv1, Yv1 = load_data(inputFile1,fnames1)
    Yt1 = Yt1.astype("int")
    Yv1 = Yv1.astype("int")

    setsT0 = split_datasets(Xt0, Yt0)
    setsV0 = split_datasets(Xv0,Yv0)

    setsT1 = split_datasets(Xt1, Yt1)
    setsV1 = split_datasets(Xv1,Yv1)

    for sets in [setsT0, setsV0, setsT1,setsV1]:
        print("trainning models")
        for i, classifier in enumerate(classifiers):
            print("trainning-testing model ",i," :",classifier_names[i])
            model, predicted, tt, tp = train_predict(sets, classifier)
            #see how model performed
            print("getting score for model ",i," :",classifier_names[i])
            if sets == setsT0:
                get_model_score("transients_dmdt0",classifier_names[i],model, predicted, sets,outputFile, tt, tp)
            elif sets == setsV0:
                get_model_score("variables_dmdt0",classifier_names[i],model, predicted, sets,outputFile, tt, tp)
            elif sets == setsT1:
                get_model_score("transients_dmdt1",classifier_names[i],model, predicted, sets,outputFile, tt, tp)
            elif sets == setsV1:
                get_model_score("variables_dmdt1",classifier_names[i],model, predicted, sets,outputFile, tt, tp)
