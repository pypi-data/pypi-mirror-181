#!/usr/bin/env python
# coding: utf-8
"""Fill NA custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class FillNa(TransformerMixin, BaseEstimator):
    """Fill Na records with a given value. 

    Parameters
    ----------
    transformers : list of tuples
        List of (column, value) tuples specifying the
        transformer objects to be applied to subsets of the data.

        column :  str
            Indexes the data on its second axis. Integers are interpreted as
            positional columns, while strings can reference DataFrame columns
            by name.  A scalar string or int should be used where
            ``transformer`` expects X to be a 1d array-like (vector),
            otherwise a 2d array will be passed to the transformer.
            A callable is passed the input data `X` and can return any of the
            above. To select multiple columns by name or dtype, you can use
            :obj:`make_column_selector`.
        value : str, int, float or Any
            The value to fill NA records;
    
    remainder : {'drop', 'passthrough'} or estimator, default='drop'
        By default, only the specified columns in `transformers` are
        transformed and combined in the output, and the non-specified
        columns are dropped. (default of ``'drop'``).
        By specifying ``remainder='passthrough'``, all remaining columns that
        were not specified in `transformers` will be automatically passed
        through. This subset of columns is concatenated with the output of
        the transformers.
        By setting ``remainder`` to be an estimator, the remaining
        non-specified columns will use the ``remainder`` estimator. The
        estimator must support :term:`fit` and :term:`transform`.
        Note that using this feature requires that the DataFrame columns
        input at :term:`fit` and :term:`transform` have identical order.

    """

    def __init__(
        self,
        transformers: list,
        remainder: str = "drop",
        inplace=False,
    ):
        self._transformers = dict(transformers)
        self.remainder = remainder
        self._inplace = inplace
        self._feature_names_out = None
    
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
        if self.remainder == "drop":
            self._feature_names_out = list(self._transformers.keys())
        else:
            self._feature_names_out = X.columns.names
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
        return self._transform(X)

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

    def _transform(self, X):
        if self._inplace:
            X.fillna(
                self._transformers, 
                inplace=self._inplace
            )
        else: # if self._inplace == false
            X = X.fillna(
                self._transformers, 
                inplace=self._inplace
            )
        return X[self._feature_names_out]

    def __sklearn_is_fitted__(self):
        """Return True since FunctionTransfomer is stateless."""
        if self._feature_names_out is not None:
            return True
        else:
            return False
