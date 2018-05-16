import numpy as np 
import pandas as pd 
from load_lc import load_lc, get_file_name, load_tagged_metadata
import itertools as it
import math
from os.path import dirname, abspath
from utils import dmranges, dtranges, dmrnames, dtrnames,fnames
import sys

featuresdf = pd.DataFrame(columns = fnames)
errorsdf = pd.DataFrame(columns=['filename','error'])

def normalized_image_intensity(nbin,p):
    i = int(225*nbin/p + 0.99999)
    return i

def get_dmdts(lc, tag, objid):
    global featuresdf
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
    content = [objid]+dm_norm+dt_norm+[tag]
    feature_row = pd.DataFrame([content], columns = fnames)
    featuresdf = pd.concat([featuresdf,feature_row], ignore_index=True)

if __name__ == "__main__":
    inputFilename = "standard-features/main-classes/tagged_metadata_main_classes.csv"
    outputname = "dmdts/main-classes/tagged_dmdts.csv"
    eoutputname = "dmdts/main-classes/errors_processing_dmdts.csv"
    data_dir = dirname(dirname(abspath(__file__)))+"/data/"

    if len(sys.argv)>1:
        inputFile = sys.argv[1]+".csv"
    if len(sys.argv)>2:
        output = sys.argv[2]+".csv"
    if len(sys.argv)>3:
        output = sys.argv[3]+".csv"

    tagged_metadata = load_tagged_metadata(inputFilename)
    
    for index, row in tagged_metadata.iterrows():
        try:
            filename, objid = get_file_name(row)
            lc = load_lc(filename)
            tag = row['tag']
            print("Trying to get dmdts for: ", filename)
            get_dmdts(lc, tag, objid)
        except Exception as e:
            print('error: ',str(e))
            print("something went wrong when trying to process file: ", filename)
            error = {'filename':[filename],'error': [str(e)]}
            error_row = pd.DataFrame(data=error)
            errorsdf = pd.concat([errorsdf, error_row],ignore_index=True)

    # save features + errors
    featuresdf.to_csv(data_dir+outputname, sep=',')
    errorsdf.to_csv(data_dir+eoutputname, sep=",")
    
    
