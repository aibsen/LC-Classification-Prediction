import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import clean_feature_list

filename = "data/clean_tagged_features.csv"
tagged_features = pd.read_csv(filename, sep=",")
# X = tagged_features[clean_feature_list]
# X=X.replace([np.inf, -np.inf], np.nan)
# where_are_nans = X.isnull()
# sum_nans = where_are_nans.sum()
# feature_nans = list(sum_nans[sum_nans[clean_feature_list]>0].keys())
# arbitrary = 10
# for fnan in feature_nans:
#     ids_nan = list(where_are_nans[where_are_nans[fnan]==True].index)      
#     try:
#         if len(ids_nan) > arbitrary:
#             tagged_features = tagged_features.drop([fnan],axis=1)
#         else:
#             tagged_features = tagged_features.drop(ids_nan)
#     except Exception as e:
#         print('error: ',str(e))
#         print('probably trying to drop value that has already been dropped')

# #remove classes Unknown/Other (6 and 8)
# tagged_features = tagged_features[(tagged_features['tag']!=6) & (tagged_features['tag']!=8)]


sns.pairplot(tagged_features, hue="tag", vars=clean_feature_list[0:5], dropna=True)
plt.show()

