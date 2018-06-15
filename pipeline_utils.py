from os.path import dirname, abspath

crts_url_list = ["http://nesssi.cacr.caltech.edu/catalina/Allns.arch.html#table1",
            "http://nesssi.cacr.caltech.edu/MLS/Allns.arch.html",
            "http://nesssi.cacr.caltech.edu/SSS/Allns.html"]

utils_dir = dirname(abspath(__file__))+"/utils/"

data_dir = dirname(abspath(__file__))+"/data/"

transient_fieldnames = ['ID', 'RA', 'Dec', 'UT Date', 'Mag', 'CSS images', 'SDSS', 'Others', 'Followed', 'Last', 'LC', 'FC', 'Classification','SubClassification']
       
variables_fieldnames = ["ID", "RA", "Dec", "Peroid", "V_CSS", "Npts", "V_amp", "SubType"]

unified_fieldnames = ["ID", "RA", "Dec", "SubType", "Type" ]

feature_list = ["amplitude",
    "anderson_darling",
    "beyond1Std",
    "eta_e",
    "mean",
    "std",
    "rcs",
    "stetsonK",
    "medianAbsDev",
    "medianBRP",
    "pairSlopeTrend",
    "percentAmplitude",
    "percentDifferenceFluxPercentile",
    "q31",
    "gskew",
    "smallKurtosis",
    "meanVariance",
    "maxSlope",
    "linearTrend",
    "autocor_length",
    "con",
    "skew",
    "fluxPercentileRatioMid20",
    "fluxPercentileRatioMid35",
    "fluxPercentileRatioMid50",
    "fluxPercentileRatioMid65",
    "fluxPercentileRatioMid80"]

clean_feature_list = ["amplitude",
    "anderson_darling",
    "beyond1Std",
    # "eta_e",
    "mean",
    "std",
    "rcs",
    # "stetsonK",
    "medianAbsDev",
    "medianBRP",
    "pairSlopeTrend",
    "percentAmplitude",
    "percentDifferenceFluxPercentile",
    "q31",
    "gskew",
    "smallKurtosis",
    "meanVariance",
    # "maxSlope",
    "linearTrend",
    "autocor_length",
    "con",
    "skew",
    "fluxPercentileRatioMid20",
    "fluxPercentileRatioMid35",
    "fluxPercentileRatioMid50",
    "fluxPercentileRatioMid65",
    "fluxPercentileRatioMid80"]

dmranges0 = [-8,-5,-3,-2.5,-2,-1.5,-1,-0.5,-0.3,-0.2,-0.1,0, 0.1, 0.2, 0.3, 0.5, 1, 1.5, 2, 2.5, 3, 5, 8]
dmranges1 = [-8,-7.8,-7.5,-7.3,-7,-6.8,-6.5,-6,-5.5,-5.0,-3.0,-1,0,1.0,3.0,5.0,5.5,6.0,6.5,6.8,7,7.3,7.5,7.8,8]
# dmranges2 = [-8,-7.5,-7,-6.5,-6,-5.5,-5,4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,0,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8]
dtranges = [1/145, 2/145, 3/145, 4/145, 1/25, 2/25, 3/25, 1.5, 2.5, 3.5,4.5,
    5.5,7,10,20,30,60,90,120,240,600,960,2000,4000]
dtrnames = ["dt-"+str(x) for x in range(len(dtranges)-1)]
dmrnames0 = ["dm-"+str(x) for x in range(len(dmranges0)-1)]
fnames0 = ["ID"]+dmrnames0+dtrnames+["Type"]+["SubType"]
dmrnames1 = ["dm-"+str(x) for x in range(len(dmranges1)-1)]
fnames1 = ["ID"]+dmrnames1+dtrnames+["Type"]+["SubType"]
# dmrnames2 = ["dm-"+str(x) for x in range(len(dmranges2)-1)]
# fnames2 = ["ID"]+dmrnames2+dtrnames+["Type"]+["SubType"]