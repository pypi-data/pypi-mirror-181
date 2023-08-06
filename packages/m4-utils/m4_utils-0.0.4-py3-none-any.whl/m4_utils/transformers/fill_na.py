#!/usr/bin/env python
# coding: utf-8
"""Fill NA custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class FillNa(TransformerMixin, BaseEstimator):
    """Constructs a transformer from an arbitrary callable.

    A FunctionTransformer forwards its X (and optionally y) arguments to a
    user-defined function or function object and returns the result of this
    function. This is useful for stateless transformations such as taking the
    log of frequencies, doing custom scaling, etc.

    Note: If a lambda is used as the function, then the resulting
    transformer will not be pickleable.

    .. versionadded:: 0.17

    Read more in the :ref:`User Guide <function_transformer>`.

    Parameters
    ----------
    func : callable, default=None
        The callable to use for the transformation. This will be passed
        the same arguments as transform, with args and kwargs forwarded.
        If func is None, then func will be the identity function.

    inverse_func : callable, default=None
        The callable to use for the inverse transformation. This will be
        passed the same arguments as inverse transform, with args and
        kwargs forwarded. If inverse_func is None, then inverse_func
        will be the identity function.

    validate : bool, default=False
        Indicate that the input X array should be checked before calling
        ``func``. The possibilities are:

        - If False, there is no input validation.
        - If True, then X will be converted to a 2-dimensional NumPy array or
          sparse matrix. If the conversion is not possible an exception is
          raised.

        .. versionchanged:: 0.22
           The default of ``validate`` changed from True to False.

    accept_sparse : bool, default=False
        Indicate that func accepts a sparse matrix as input. If validate is
        False, this has no effect. Otherwise, if accept_sparse is false,
        sparse matrix inputs will cause an exception to be raised.

    check_inverse : bool, default=True
       Whether to check that or ``func`` followed by ``inverse_func`` leads to
       the original inputs. It can be used for a sanity check, raising a
       warning when the condition is not fulfilled.

       .. versionadded:: 0.20

    feature_names_out : callable, 'one-to-one' or None, default=None
        Determines the list of feature names that will be returned by the
        `get_feature_names_out` method. If it is 'one-to-one', then the output
        feature names will be equal to the input feature names. If it is a
        callable, then it must take two positional arguments: this
        `FunctionTransformer` (`self`) and an array-like of input feature names
        (`input_features`). It must return an array-like of output feature
        names. The `get_feature_names_out` method is only defined if
        `feature_names_out` is not None.

        See ``get_feature_names_out`` for more details.

        .. versionadded:: 1.1

    kw_args : dict, default=None
        Dictionary of additional keyword arguments to pass to func.

        .. versionadded:: 0.18

    inv_kw_args : dict, default=None
        Dictionary of additional keyword arguments to pass to inverse_func.

        .. versionadded:: 0.18

    Attributes
    ----------
    n_features_in_ : int
        Number of features seen during :term:`fit`. Defined only when
        `validate=True`.

        .. versionadded:: 0.24

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Defined only when `validate=True`
        and `X` has feature names that are all strings.

        .. versionadded:: 1.0

    See Also
    --------
    MaxAbsScaler : Scale each feature by its maximum absolute value.
    StandardScaler : Standardize features by removing the mean and
        scaling to unit variance.
    LabelBinarizer : Binarize labels in a one-vs-all fashion.
    MultiLabelBinarizer : Transform between iterable of iterables
        and a multilabel format.

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.preprocessing import FunctionTransformer
    >>> transformer = FunctionTransformer(np.log1p)
    >>> X = np.array([[0, 1], [2, 3]])
    >>> transformer.transform(X)
    array([[0.       , 0.6931...],
           [1.0986..., 1.3862...]])
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
