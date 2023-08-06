# -*- coding: utf-8 -*-
"""
module utils.py
----------------------
 A set of Utility functions and classes.
"""
import sys
import os
from datetime import datetime
import numpy as np
import pandas as pd
import json


class TimeIt(object):
    """ A context manager for measuring displaing operations elapsed time. 
    """
    
    def __enter__(self):
        self.started_at = datetime.now()
    
    def __exit__(self, *args, **kwargs):
        self.elapsed_time = datetime.now() - self.started_at


class NumpyEncoder(json.JSONEncoder):
    """
    A JSONEncoder sub-class that serializes numpy arrays.
    To use this encoder instead of the default json encoder you must call json.dump or json.dumps
    passing this class to the 'cls' optional named parameter as the follows.
    ```
        json.dumps(array, cls=NumpyEncoder)
    ```
    """
    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.core.floating):
            return float(o)
        if isinstance(o, np.core.signedinteger):
            return int(o)

        return json.JSONEncoder.default(self, o)
             
            
        