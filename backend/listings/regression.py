import numpy as np

"""
Simple function to get the trend for a set of data

if the slope is a +ve value --> increasing trend

if the slope is a -ve value --> decreasing trend

if the slope is a zero value --> No trend
"""
def trendline(index,data, order=1):
    coeffs = np.polyfit(index, list(data), order)
    slope = coeffs[-2]
    return float(slope)
