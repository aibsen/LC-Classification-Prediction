import numpy as np
import pandas as pd
import csv
import importlib
import feature_functions as f

feature_list = ["amplitude", "anderson_darling_test", "eta_e", "mean", "std", 
    "rcs", "mean_variance", "medianAbsDev", "medianBRP", "pairSlopeTrend",
    "percentAmplitude","percentDifferenceFluxPercentile", "q31", "gskew", "smallKurtosis",
    "meanVariance", "maxSlope", "linearTrend"]
function_list = [getattr(f, x) for x in feature_list]

def get_features():
    featuresdf = pd.DataFrame(columns=feature_list)
#iterate over files

    data = pd.read_csv("data0/703201120684101938", sep=",", names=["coords", "time", "mag", "error"], skiprows=1)
    mag = data['mag']
    time = pd.to_numeric(data["time"].str.split("(").str[0])
    error = data["error"]
    clean_data = clean(mag.tolist(),time.tolist(),error.tolist())
    lc = np.array(clean_data)
    features = list(map(lambda f: f(lc), function_list))
    featuresdf = pd.concat([featuresdf, pd.DataFrame([features],columns=feature_list)],  ignore_index=True)
    print(featuresdf)


def clean(mag,time,error):
    m = np.mean(error)
    clean_date = []
    clean_mag = []
    clean_error = []	
    for i in range(len(mag)):
        if error[i] < (3 * m) and (np.absolute(mag[i] - np.mean(mag)) / np.std(mag)) < 5 :
            clean_date.append(time[i])
            clean_mag.append(mag[i])
            clean_error.append(error[i])
    clean_mag = np.asarray(clean_mag)	
    clean_date = np.asarray(clean_date)	
    clean_error = np.asarray(clean_error)	
    return [clean_mag, clean_date, clean_error]

get_features()
