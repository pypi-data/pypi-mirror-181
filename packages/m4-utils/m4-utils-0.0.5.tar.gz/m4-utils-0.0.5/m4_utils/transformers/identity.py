#!/usr/bin/env python
# coding: utf-8
"""Identity custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin, OneToOneFeatureMixin


class Identity(OneToOneFeatureMixin, TransformerMixin, BaseEstimator):
    """Identity transformer.
    """

    def __init__(self):
        pass
    
    def fit(self, X: pd.DataFrame, y=None):
        """Fit transformer by checking X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            FillNa transformer class instance.
        """
        return self

    def transform(self, X):
        """Identity Transformation of X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        return X

    def inverse_transform(self, X):
        """Transform X using the inverse function.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        return X

