import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys
from os.path import dirname, abspath
import matplotlib.pyplot as plt

classifier_names = ["Nearest Neighbors", "RBF SVM", 
# "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]


def plot_results(scores, times, data_dir):
    data = {
        'score': scores,
        'time': times,
        'model': classifier_names
    }
    print(data)
    score_plot = sns.barplot(x="score", y="model", data=data).get_figure()
    score_plot.savefig(data_dir+"score-plot.png")

    time_plot = sns.barplot(x="time", y="model", data=data).get_figure()
    time_plot.savefig(data_dir+"time-plot.png")

    
def load_result(subdir):
    main_dir = dirname(dirname(abspath(__file__)))
    data_dir = main_dir+"/results/"+subdir+"/"
    time = []
    score = []
    for classifier in classifier_names:
        inputFile = data_dir+classifier+".txt"
        f = open(inputFile,"r") 
        for line in f:
            if "mean_score" in line:
                mean_score = line.split(":")[1]
                score.append(float(mean_score))
            if ("time" in line) and ("train" in line):
                mean_time = line.split(":")[1]
                time.append(float(mean_time))
        f.close()
    plot_results(score, time, data_dir)
    

if __name__ == "__main__":
    subdir =""
    if len(sys.argv)>1:
        subdir = sys.argv[1]
        results = load_result(subdir)
        
    
    

