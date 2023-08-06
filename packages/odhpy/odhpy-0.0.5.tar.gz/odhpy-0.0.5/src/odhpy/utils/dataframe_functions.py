import pandas as pd
from odhpy import utils
from pandas.api.types import is_datetime64_any_dtype as is_datetime


def set_index_dt(df: pd.DataFrame, dt_values=None, start_dt=None, cancel_if_index_are_datetimes=True):
    """
    Returns a dataframe with datetimes as the index.     
    If no optional arguments are provided, the function will look for a column named "Date" (not 
    case-sensitive) within the input dataframe. Otherwise dt_values or start_dt (assumes daily)
    may be provided. 

    Args:
        df (pd.DataFrame): _description_
        dt_values (_type_, optional): _description_. Defaults to None.
        start_dt (_type_, optional): _description_. Defaults to None.
        cancel_if_index_are_datetimes (bool, optional): _description_. Defaults to True.
    """
    if cancel_if_index_are_datetimes and is_datetime(df.index):
        return df
    
    if start_dt != None:
        df["Date"] = utils.get_dates(start_dt, days=len(df))    
    elif dt_values != None:
        nn = len(df)
        if len(dt_values) < nn:
            raise Exception("dt_values is shorter than the dataframe.") 
        df["Date"] = dt_values[:nn]
 
    col = [c for c in df.columns if c.upper().strip() == "DATE"]
    if len(col) > 0:
        df["Date"] = pd.to_datetime(df[col[0]])
        answer = df.set_index("Date")
        return answer
    else:
        raise Exception("Could not find 'Date' column.")
