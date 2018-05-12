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

feature_nans = ['eta_e', 'stetsonK', 'maxSlope']
clean_feature_list = [x for x in feature_list if x not in feature_nans]

feature_list1 = ['amplitude','beyond1Std',"medianBRP","fluxPercentileRatioMid50",
    "fluxPercentileRatioMid65","q31","gskew"]

feature_list2 = ['gskew','q31',"medianBRP","medianAbsDev",
    "percentDifferenceFluxPercentile","fluxPercentileRatioMid50"]

feature_list3 = [
    "anderson_darling",
    "rcs",
    "pairSlopeTrend",
    "percentAmplitude",
    "percentDifferenceFluxPercentile",
    "q31",
    "gskew",
    "con",
    "fluxPercentileRatioMid50"]


feature_list4 = ["amplitude",
    "anderson_darling",
    "beyond1Std",
    "mean",
    "std",
    "rcs",
    "mean_variance",
    "medianAbsDev",
    "medianBRP",
    "pairSlopeTrend",
    "percentAmplitude",
    "percentDifferenceFluxPercentile",
    "fluxPercentileRatioMid80"]

feature_list5 = ["amplitude",
    "anderson_darling",
    "beyond1Std",
    "mean",
    "std",
    "rcs",
    "mean_variance",
    "medianAbsDev",
    "medianBRP",
    "pairSlopeTrend",
    "percentAmplitude",
    "percentDifferenceFluxPercentile",
    "smallKurtosis",
    "maxSlope",
    "linearTrend",
    "autocor_length",
    "fluxPercentileRatioMid20",
    "fluxPercentileRatioMid35",
    "fluxPercentileRatioMid50",
    "fluxPercentileRatioMid65",
    "fluxPercentileRatioMid80"]

feature_list6 = ["amplitude",
    "anderson_darling",
    "rcs",
    "pairSlopeTrend",
    "percentAmplitude",
    "percentDifferenceFluxPercentile",
    "q31",
    "gskew",
    "smallKurtosis",
    "meanVariance",
    "maxSlope",
    "con",
    "fluxPercentileRatioMid35",
    "fluxPercentileRatioMid50",
    "fluxPercentileRatioMid65",
    "fluxPercentileRatioMid80"]


# VarianceThreshold 80%: 
vt80 =[
    'amplitude', 'mean', 'std', 'q31', 'gskew', 'smallKurtosis', 'autocor_length', 'skew']
# SelectKBest(k=5): 
skb  =['amplitude', 'std', 'percentDifferenceFluxPercentile', 'q31', 'meanVariance']
# SelectKBest(mutual_info_classif, k=5): 
skbm =['amplitude', 'mean', 'percentDifferenceFluxPercentile', 'gskew', 'meanVariance']
# SelectPercentile 25: 
sp25 =['amplitude', 'mean', 'std', 'percentDifferenceFluxPercentile', 'q31', 'meanVariance']
# GenericUnivariateSelect: 
gus = ['meanVariance']
# GenericUnivariateSelect(mutual_info_classif): 
gusm=['gskew']
#both above
gus2 = ['meanVariance', "gskew"]
