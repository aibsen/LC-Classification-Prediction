import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

scores = {'score':[0.658,0.633,0.703,0.522,0.671,0.693,0.214,0.721,0.702],
    'time':[0.861, 0.164,878.105,0.002, 0.011,0.693,0.0325,0.211,2.105],
    'model':['AdaBoost','Decision Tree','Gaussian Process','Naive Bayes','Nearest Neighbors', 'NN','QDA','Random Forest','RBF SVM']}

score_df = pd.DataFrame(data=scores)
print(score_df)
# ax = sns.barplot(x="score", y="model", data=scores)
ax = sns.barplot(x="time", y="model", data=scores)
plt.show()
