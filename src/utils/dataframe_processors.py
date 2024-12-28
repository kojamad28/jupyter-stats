import numpy as np
import pandas as pd


def get_value_from_dataframe(data, data_type, empty_value=np.nan):

    if isinstance(data, pd.Series):
        if data.empty:
            return empty_value
        else:
            return data.values[0]
    elif isinstance(data, data_type):
        return data
    else:
        raise TypeError(f'{data} should be {data_type} or pd.Series.')
