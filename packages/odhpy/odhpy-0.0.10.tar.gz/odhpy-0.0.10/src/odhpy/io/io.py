import pandas as pd
from odhpy import utils

def read_ts_csv(filename, date_format=r"%d/%m/%Y", df=None, colprefix="", **kwargs):
    """Reads a daily timeseries csv into a DataFrame, and sets the index to the Date.
    Assumed there is a column named "Date"

    Args:
        filename (_type_): _description_
        date_format (str, optional): defaults to "%d/%m/%Y" as per Fors. Other common formats include "%Y-%m-%d", "%Y/%m/%d".

    Returns:
        _type_: _description_
    """
    if df is None:
        df = pd.DataFrame()
    temp = pd.read_csv(filename, **kwargs)
    temp = utils.set_index_dt(temp, format=date_format)
    if colprefix is not None:
        for c in temp.columns:
            temp.rename(columns = {c:f"{colprefix}{c}"}, inplace = True)        
    df = df.join(temp, how="outer").sort_index()
    # TODO: THERE IS NO GUARANTEE THAT THE DATES OVERLAP, THEREFORE WE MAY END UP WITH A DATAFRAME WITH INCOMPLETE DATES
    return df