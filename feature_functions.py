import time
import math
import numpy as np
import pandas as pd
from scipy import stats


def amplitude(data):
    magnitude = data[0]
    N = len(magnitude)
    sorted_mag = np.sort(magnitude)

    return (np.median(sorted_mag[-int(math.ceil(0.05 * N)):]) -
            np.median(sorted_mag[0:int(math.ceil(0.05 * N))])) / 2.0

def anderson_darling_test(data):
    magnitude = data[0]
    ander = stats.anderson(magnitude)[0]
    return 1 / (1.0 + np.exp(-10 * (ander - 0.3)))


# def beyond1Std(data):

#     magnitude = data[0]
#     error = data[2]
#     n = len(magnitude)

#     weighted_mean = np.average(magnitude, weights=1 / error ** 2)

#     # Standard deviation with respect to the weighted mean

#     var = sum((magnitude - weighted_mean) ** 2)
#     std = np.sqrt((1.0 / (n - 1)) * var)

#     count = np.sum(np.logical_or(magnitude > weighted_mean + std,
#                                     magnitude < weighted_mean - std))

#     return float(count) / n

def eta_e(data):

    magnitude = data[0]
    time = data[1]
    w = 1.0 / np.power(np.subtract(time[1:], time[:-1]), 2)
    w_mean = np.mean(w)
    N = len(time)
    sigma2 = np.var(magnitude)
    S1 = sum(w * (magnitude[1:] - magnitude[:-1]) ** 2)
    S2 = sum(w)
    eta_e = (w_mean * np.power(time[N - 1] -
                time[0], 2) * S1 / (sigma2 * S2 * N ** 2))
    return eta_e


def mean(data):
    magnitude = data[0]
    mean = np.mean(magnitude)
    return mean

def std(data):
    magnitude = data[0]
    return np.std(magnitude)

def rcs(data):
    magnitude = data[0]
    sigma = np.std(magnitude)
    N = len(magnitude)
    m = np.mean(magnitude)
    s = np.cumsum(magnitude - m) * 1.0 / (N * sigma)
    R = np.max(s) - np.min(s)
    return R

# def stetsonK(data):
#     magnitude = data[0]
#     error = data[2]
#     mean_mag = (np.sum(magnitude/(error*error)) /
#                 np.sum(1.0 / (error * error)))
#     N = len(magnitude)
#     sigmap = (np.sqrt(N * 1.0 / (N - 1)) *
#                 (magnitude - mean_mag) / error)
#     K = (1 / np.sqrt(N * 1.0) *
#             np.sum(np.abs(sigmap)) / np.sqrt(np.sum(sigmap ** 2)))
#     return K

def mean_variance(data):
    magnitude = data[0]
    return np.std(magnitude) / np.mean(magnitude)


def medianAbsDev(data):
    magnitude = data[0]
    median = np.median(magnitude)
    devs = (abs(magnitude - median))
    return np.median(devs)

def medianBRP(data):
    magnitude = data[0]
    median = np.median(magnitude)
    amplitude = (np.max(magnitude) - np.min(magnitude)) / 10
    n = len(magnitude)

    count = np.sum(np.logical_and(magnitude < median + amplitude,
                                    magnitude > median - amplitude))

    return float(count) / n


def pairSlopeTrend(data):
    magnitude = data[0]
    data_last = magnitude[-30:]
    return (float(len(np.where(np.diff(data_last) > 0)[0]) -
            len(np.where(np.diff(data_last) <= 0)[0])) / 30)


def percentAmplitude(data):
    magnitude = data[0]
    median_data = np.median(magnitude)
    distance_median = np.abs(magnitude - median_data)
    max_distance = np.max(distance_median)

    percent_amplitude = max_distance / median_data

    return percent_amplitude

def percentDifferenceFluxPercentile(data):
    magnitude = data[0]
    median_data = np.median(magnitude)

    sorted_data = np.sort(magnitude)
    lc_length = len(sorted_data)
    F_5_index = int(math.ceil(0.05 * lc_length))
    F_95_index = int(math.ceil(0.95 * lc_length))
    F_5_95 = sorted_data[F_95_index] - sorted_data[F_5_index]

    percent_difference = F_5_95 / median_data

    return percent_difference

def q31(data):
    magnitude = data[0]
    return np.percentile(magnitude, 75) - np.percentile(magnitude, 25)

def gskew(data):
    magnitude = np.array(data[0])
    median_mag = np.median(magnitude)
    F_3_value = np.percentile(magnitude, 3)
    F_97_value = np.percentile(magnitude, 97)

    return (np.median(magnitude[magnitude <= F_3_value]) +
            np.median(magnitude[magnitude >= F_97_value])
            - 2*median_mag)

def smallKurtosis(data):
    magnitude = data[0]
    n = len(magnitude)
    mean = np.mean(magnitude)
    std = np.std(magnitude)

    S = sum(((magnitude - mean) / std) ** 4)

    c1 = float(n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))
    c2 = float(3 * (n - 1) ** 2) / ((n - 2) * (n - 3))

    return c1 * S - c2

def meanVariance(data):
    magnitude = data[0]
    return np.std(magnitude) / np.mean(magnitude)

def maxSlope(data):

    magnitude = data[0]
    time = data[1]
    slope = np.abs(magnitude[1:] - magnitude[:-1]) / (time[1:] - time[:-1])
    np.max(slope)

    return np.max(slope)

def linearTrend(data):
    magnitude = data[0]
    time = data[1]
    regression_slope = stats.linregress(time, magnitude)[0]
    return regression_slope