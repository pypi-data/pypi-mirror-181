#!/usr/bin/env python
# coding: utf-8
"""Time normalization custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class CustomTimeNormalization(TransformerMixin, BaseEstimator):
    """Custom Time Column nomalization; 

    Parameters
    ----------
    columns : list of tuples
        List of (value_column, mean_column, std_column, out_name) tuples specifying the
        transformer objects to be applied to subsets of the data.

        value_column :  str
            The name of the column to be normalized.
        mean_column :  str
            The name of the column to be used as mean.

        std_column :  str
            The name of the column to be used as std.
        
        out_name : str
            Normalized Column output name;
    """

    def __init__(
        self,
        columns: list
    ):
        self._columns = columns
        self._feature_names_out = [
            c[3] if len(c) == 4 else c[2]
            for c in self._columns
        ]
    
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
        """Transform X using the forward function.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        res = dict()
        for columns, c_name in zip(self._columns, self._feature_names_out):
            amount, mean, std = columns[0], columns[1], columns[2]
            res[c_name] = self._transform(X[amount], X[mean], X[std])
        return pd.DataFrame(data=res)

    def inverse_transform(self, X):
        """[NOT IMPLEMENTED] Transform X using the inverse function.

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

    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        This method is only defined if `feature_names_out` is not None.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Input feature names.

            - If `input_features` is None, then `feature_names_in_` is
              used as the input feature names. If `feature_names_in_` is not
              defined, then names are generated:
              `[x0, x1, ..., x(n_features_in_ - 1)]`.
            - If `input_features` is array-like, then `input_features` must
              match `feature_names_in_` if `feature_names_in_` is defined.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.

            - If `feature_names_out` is 'one-to-one', the input feature names
              are returned (see `input_features` above). This requires
              `feature_names_in_` and/or `n_features_in_` to be defined, which
              is done automatically if `validate=True`. Alternatively, you can
              set them in `func`.
            - If `feature_names_out` is a callable, then it is called with two
              arguments, `self` and `input_features`, and its return value is
              returned by this method.
        """
        return np.asarray(
            self._feature_names_out, 
            dtype=object
        )

    def _transform(self, amount, amount_mean, amount_std):
        amount_std = amount_std.copy()
        amount_std.loc[amount_std == 0.] = 0.001
        return ((amount - amount_mean) / amount_std).astype('float32')
        
    def __sklearn_is_fitted__(self):
        """Return True since FunctionTransfomer is stateless."""
        return True
