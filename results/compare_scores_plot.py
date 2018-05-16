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
# feature_names = ["vt80","sp25","skbm","skb","ranked","pca5","pca10","pca15","gus2","dmdts","all-features"]
columns=['fname','classifier','score']
feature_names = ["ranked","pca5","pca10","pca15","dmdts","all-features"]

results_df = pd.DataFrame(columns=columns)

#put together df with all results from main classes 

def load_result(result_dir):
    global results_df
    time = []
    score = []
    for f_name in feature_names:
        for classifier in classifier_names:
            inputFile = result_dir+f_name+"/"+classifier+".txt"
            f = open(inputFile,"r") 
            for line in f:
                if "mean_score" in line:
                    mean_score = line.split(":")[1]
                    mean_score = float(mean_score)
                    content = [f_name,classifier,mean_score]
                    row = pd.DataFrame([content], columns = columns)
                    results_df = pd.concat([results_df,row], ignore_index=True)
            f.close()
    return results_df    

def plot_results(results):
    sns.set(style="whitegrid")
    palette = sns.color_palette("Set1", 8, .8)
    plot = sns.factorplot(x="fname",y="score", hue="classifier",kind="bar",
        palette=palette, data=results, size=8, aspect=3.5 )
    plot.despine(left=True)
    plot.set_xlabels("Features used")
    plt.show()

if __name__ == "__main__":
    main_dir = dirname(dirname(abspath(__file__)))
    subdir = "main-classes"
    if len(sys.argv)>1:
        subdir = sys.argv[1]

    result_dir = main_dir+"/results/"+subdir+"/"
    results = load_result(result_dir)
    plot_results(results)