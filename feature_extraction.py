import numpy as np
import pandas as pd
import csv
import importlib
import feature_functions as f

feature_list = ["amplitude", "anderson_darling_test", "eta_e", "mean", "std", 
    "rcs", "mean_variance", "medianAbsDev", "medianBRP", "pairSlopeTrend",
    "percentAmplitude", "q31", "gskew", "smallKurtosis",
    "meanVariance", "maxSlope", "linearTrend"]
function_list = [getattr(f, x) for x in feature_list]
featuresdf = pd.DataFrame(columns=feature_list)

def get_features(filename,tag):
    global featuresdf
    data = pd.read_csv(filename, sep=",", names=["coords", "time", "mag", "error"], skiprows=1)
    mag = data['mag']
    time = pd.to_numeric(data["time"].str.split("(").str[0])
    error = data["error"]
    clean_data = clean(mag.tolist(),time.tolist(),error.tolist())
    lc = np.array(clean_data)
    features = list(map(lambda f: f(lc), function_list))
    row = pd.DataFrame([features],columns=feature_list)
    row['tag'] = tag
    featuresdf = pd.concat([featuresdf, row],  ignore_index=True)

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


if __name__ == "__main__":

    fieldnames =  ["ID","RA (J2000)","Dec (J2000)","UT Date","Mag","images","SDSS",
        "Others","Followed","Last","LC","FC","Classification","SubClassification","Survey","tag"]
    tagged_metadata = pd.read_csv("tagged_meta_data.csv", sep=",", names=fieldnames, skiprows=1)
    for index, row in tagged_metadata.iterrows():
        filename = ""
        tag = row['tag']
        if row['Survey'] == 'CSS':
            filename = "data0/"+str(row['images'])
        elif row['Survey'] == 'MLS':
            filename = "data1/"+str(row['images'])
        elif row['Survey'] == 'SSS':
            filename = "data2/"+str(row['images'])
        try:
            print("Trying to get features for: ", filename)
            get_features(filename, tag)
        except Exception as e:
            print('error: ',str(e))
            print("something went wrong when trying to process file: ", filename)
    
    #save features
    # featuresdf.to_csv("tagged_features.csv", sep=',')
    #removed 'percentDifferenceFluxPercentile' on the second run because it gave too many errors with short lc vectors
    featuresdf.to_csv("tagged_features2.csv", sep=',')
        
    
