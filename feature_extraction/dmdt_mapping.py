import numpy as np 
import pandas as pd 
from load_lc import load_lc, get_file_name, load_tagged_metadata
import itertools as it
import math


dmranges = [0, 0.1, 0.2, 0.3, 0.5, 1, 1.5, 2, 2.5, 3, 5, 8]
dtranges = [1/145, 2/145, 3/145, 4/145, 1/25, 2/25, 3/25, 1.5, 2.5, 3.5,4.5,
    5.5,7,10,20,30,60,90,120,240,600,960,2000,4000]
dmrnames = ["dm-"+str(x) for x in range(len(dmranges)-1)]
dtrnames = ["dt-"+str(x) for x in range(len(dtranges)-1)]
fnames = ["id"]+dmrnames+dtrnames+["tag"]
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
    inputFilename = "tagged_meta_data.csv"
    outputname = "tagged_dmdts.csv"
    eoutputname = "errors_processing_dmdts.csv"
   
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

    data_dir = dirname(dirname(abspath(__file__)))+"/data/"
    # save features + errors
    featuresdf.to_csv(data_dir+outputname, sep=',')
    errorsdf.to_csv(data_dir+eoutputname, sep=",")
    
    
