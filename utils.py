feature_list = ["amplitude",
    "anderson_darling",
    "beyond1Std",
    "eta_e",
    "mean",
    "std",
    "rcs",
    "stetsonK",
    "mean_variance",
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

feature_nans = ['eta_e', 'stetsonK', 'maxSlope']
clean_feature_list = [x for x in feature_list if x not in feature_nans]