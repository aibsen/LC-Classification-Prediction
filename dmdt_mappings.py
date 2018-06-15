import numpy as np 
import pandas as pd 
from load_lc import load_lc, get_file_name
import itertools as it
import math
from pipeline_utils import dmranges0,dmranges1, dtranges,fnames0, fnames1
import sys

featuresdf0 = pd.DataFrame(columns = fnames0)
featuresdf1 = pd.DataFrame(columns = fnames1)
# featuresdf2 = pd.DataFrame(columns = fnames2)

def normalized_image_intensity(nbin,p):
    i = int(225*nbin/p + 0.99999)
    return i

def get_dmdts(lc, tag1,tag2, objid,dmranges,fnames):
    #n = number of points in the light curve
    n = lc.shape[1]
    #p = number of dm and dt for each pair of points
    p = (n*(n-1))/2
    ms = lc[0]
    ts = lc[1]
    #calculate dm
    dms = [abs(y - x) for x, y in it.combinations(ms, 2)]
    binsdm = np.histogram(dms, bins=dmranges)
    #calculate dt
    dts = [abs(y - x) for x, y in it.combinations(ts, 2)]
    binsdt = np.histogram(dts, bins=dtranges)
    #normalize image intensity so it's at most 225
    dm_norm =[normalized_image_intensity(bin, p) for bin in binsdm[0]]
    dt_norm =[normalized_image_intensity(bin, p) for bin in binsdt[0]]
    content = [objid]+dm_norm+dt_norm+[tag1]+[tag2]
    print(content)
    print(fnames)
    feature_row = pd.DataFrame([content], columns = fnames)
    return feature_row

def dmdt_mappings(inputFile,outputFile):
    global featuresdf0, featuresdf1, featuresdf2
    tagged_metadata = pd.read_pickle(inputFile)
    for index, row in tagged_metadata.iterrows():
        # try:
        dirname, filename = get_file_name(row)
        lc = load_lc(dirname,filename)
        tag1 = row['Type']
        tag2 = row['SubType']
        objid = row["ID"]
        print("Trying to get dmdts for: ", filename)
        row0=get_dmdts(lc, tag1,tag2, objid,dmranges0,fnames0)
        featuresdf0 = pd.concat([featuresdf0,row0], ignore_index=True)

        row1=get_dmdts(lc, tag1,tag2, objid,dmranges1,fnames1)
        featuresdf1 = pd.concat([featuresdf1,row1], ignore_index=True)
        # get_dmdts(lc, tag1,tag2, objid,dmranges2,fnames2,featuresdf2)
        # except Exception as e:
        #     print('error: ',str(e))
        #     print("something went wrong when trying to process file: ", filename)

    # save features + errors
    featuresdf0.to_pickle(outputFile+"0.pkl")
    featuresdf1.to_pickle(outputFile+"1.pkl")
    # featuresdf2.to_pickle(outputFile+"2.pkl", sep=',')
    
    
