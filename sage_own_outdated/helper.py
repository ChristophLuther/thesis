# helper file for own_sage.py
import numpy as np


def rf_marginal(X, model):
    """Marginal Prediction of model, i.e. without any feature in current coalition"""
    # input is an df transformed to 2d np array
    n = len(X)
    return (sum(model.predict_proba(X))) / n  # array of probabilities
