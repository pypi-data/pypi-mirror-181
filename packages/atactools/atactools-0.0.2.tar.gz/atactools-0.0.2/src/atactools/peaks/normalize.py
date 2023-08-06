# File Name: normalize.py
# Created By: ZW
# Created On: 2022-11-04
# Purpose: defines functions for normalizing peak scores to compare across samples


# module imports
# ----------------------------------------------------------------------------
from math import sqrt
from operator import attrgetter
from random import gauss, seed
from statistics import fmean, median


# module constants 
# ----------------------------------------------------------------------------
STRATEGIES = ["map", "none"]

# function definitions
# ----------------------------------------------------------------------------

# function extract_scores() which returns a list of scores given a list of
# objects with variable attribute representing the score field which can be any
# string, so long as it matches an underlying attribute name
def extract_scores(objs, field_name="score"):
    score_getter = attrgetter(field_name)
    return [score_getter(obj) for obj in objs]


# function set_scores() which applies a set of scores to a set of objects
# of the same length. This function can be used to apply normalized scores 
# back to objects after they were extracted and processed. 
def set_scores(objs, scores, field_name="score"):
    def score_setter(obj, value): obj.__dict__[field_name] = value 
    [score_setter(obj, score) for obj, score in zip(objs, scores)]


# generator object pointmap() acts similarly to numpy linspace. its only argument
# is the number of points to return, it will return that number of equidistant 
# floats on the interval (0,1)
def regular_pointmap(n, start=0.0, end=1.0, rounderr=5):
    dist = end / (n + 1)
    last = start
    while last + dist < end:
        yield round(last + dist, rounderr)
        last += dist


# function normalize_peaks_map() normalizes the peaks through a process of 
# ranking peaks by score, then assigning them to a uniform map across the interval
# (0,1). This method makes peaksets with different dynamic score ranges more
# comprable by using a rank-based approximate normalization.
def normalize_peaks_map(objs, field_name="score"):
    objs.sort(key=attrgetter(field_name)) # sort the objects by score -low to high
    set_scores(objs, scores=list(regular_pointmap(len(objs))), field_name="norm_score")
    objs.sort() # return to chromosome/positional ordering
    return objs

# define a function normalize_peaks_none() which does not normalize scores but acts
# as a placeholder identity function for the subsequent normalize_peaks function
def normalize_peaks_none(objs, field_name):
    scores = extract_scores(objs, field_name)
    set_scores(objs, scores=scores, field_name="norm_score")
    objs.sort()
    return objs

# define function normalize_peaks() which takes as input a set of objects, a field name
# to represent the underlying scores and a method argument which selects the underlying
# normalization algorithm
def  normalize_peaks(objs, field_name="score", method="map"):
    methods = {
        "map": normalize_peaks_map,
        "none": normalize_peaks_none
    }
    return methods[method](objs, field_name)