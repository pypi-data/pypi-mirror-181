from typing import Iterable
import numpy as np
from difflib import get_close_matches
import re
import mimetypes
from werkzeug.datastructures import FileStorage
import tempfile
import pandas as pd
import json
from typing import Union, List, Tuple


"""
    File name: dataframes.py
    Author: Jacob Gerlach
    Description: Assortment of basic pandas DataFrame cleaning operations.
    Notes:
        * = Function has associated unit test.
"""

def drop_val(df, col_name, value):  # *
    """Drops row from df where column entry is equal to value.

    Args:
        df (pandas DataFrame): DataFrame containing rows to drop.
        col_name (str): Name of column to investigate.
        value (pandas object): Value to drop instances of.

    Returns:
        pandas DataFrame: DataFrame with rows dropped.
    """
    return pull_not_val(df, col_name, value).reset_index(drop=True)

def pull_val(df, col_name, value):  # *
    """Retrieves rows from df where column entry is equal to value.

    Args:
        df (pandas DataFrame): DataFrame containing rows to pull.
        col_name (str): Name of column to investigate.
        value (pandas object): Value to pull instances of.

    Returns:
        pandas DataFrame: DataFrame where value is found.
    """
    return df.where(df[col_name] == value).dropna()

def pull_not_val(df, col_name, value):  # *
    """Retrieves rows from df where column entry is not equal to value.

    Args:
        df (pandas DataFrame): DataFrame containing rows to pull.
        col_name (str): Name of column to investigate.
        value (pandas object): Value to not pull instances of.

    Returns:
        pandas DataFrame: DataFrame where value is not found.
    """
    return df.where(df[col_name] != value).dropna()

def id_nearest_col(df, name, similarity_ratio=0.5, case_insensitive=True):  # *
    """Sends closest column to input column name provided that it is at least 50% similar. CASE INSENSITIVE.

    Args:
        df (pandas DataFrame): DataFrame containing header with columns of interest.
        name (str): Column name to search for.
        case_insensitive (bool, optional): If True, converts both to lower before comparing. Defaults to True.

    Returns:
        str: Most similar column name.
    """
    
    # Convert both to lowercase
    if case_insensitive:
        df_head = [col.lower() for col in df]
        name = name.lower()
    else:
        df_head = df.columns
    
    # Find closest match
    matches = get_close_matches(name, df_head, n=1, cutoff=similarity_ratio)
    if len(matches) <= 0:
        return None
    else:
        match_index = df_head.index(matches[0])
        return df.columns[match_index]
    
def remove_header_chars(df, chars, case_insensitive=True):  # *
    """Removes chars in string from df header.

    Args:
        df (pandas DataFrame): DataFrame containing header with chars to remove.
        chars (str): Continuous string of chars to individually remove.
        case_insensitive (bool, optional): If True, converts both to lower before comparing. Defaults to True.

    Returns:
        pandas DataFrame: DataFrame with header chars removed.
    """
    df = df.copy()
    
    # Convert both to lowercase
    if case_insensitive:
        chars += chars.upper() + chars.lower()
    
    for column_name in df.columns:
        translate_remove = column_name.maketrans('', '', chars)
        new_column_name = column_name.translate(translate_remove)
        df.rename(columns={column_name: new_column_name}, inplace=True)

    return df

def convert_to_nan(df, na=('', 'nan', 'none')):  # *
    """Converts all instances found in na to np.nan. Case insensitive.

    Args:
        df (pandas DataFrame): Input DataFrame
        na (iterable, optional): Contains patterns to convert. Defaults to ('', 'nan', 'none').

    Returns:
        pandas DataFrame: DataFrame replaced to nan.
    """
    na = [s.lower() for s in na]
    return df.applymap(lambda s: np.nan if str(s).lower() in na else s)

def non_num_to_nan(df, columns):  # *
    """Removes all non numeric (0-9) characters from columns specified.

    Args:
        df (pandas DataFrame): Contains non-numeric values.

    Returns:
        pandas DataFrame: Non-numerics replaced w np.nan.
    """
    
    # Cast to dataframe in case series (1 column)
    try:
        df = df[columns].applymap(lambda s: re.sub('[^0-9]', '', str(s))).replace('', np.nan)
    except AttributeError: 
        df[columns] = df[columns].map(lambda s: re.sub('[^0-9]', '', s)).replace('', np.nan)
        
    return df

def nan_col_indices(df, column_name):  # *
    # replace_blanks_w_na(df)
    return df[df[column_name].isnull()].index.tolist()

def remove_nan_cols(df):  # *
    """Removes columns that are ENTIRELY blank or NaN.

    Args:
        df (pandas DataFrame): DataFrame containing columns to drop.

    Returns:
        pandas DataFrame: DataFrame with columns dropped.
    """
    return convert_to_nan(df).dropna(axis=1, how="all")

def remove_nan_rows(df, value_column_names):  # *
    """Removes entire rows from df where value columns are blank or NaN.

    Args:
        df (pandas DataFrame): DataFrame containing column with NaN values.
        value_column_name (iterable): Contains column names to look for.

    Returns:
        pandas DataFrame: DataFrame with rows dropped where value is NaN.
    """
    return df.dropna(axis=0, subset=value_column_names).reset_index(drop=True)

def store_df(df, ext):
    
    buffer = tempfile.NamedTemporaryFile()
    if ext == 'csv':
        df.to_csv(buffer, index=False)
    elif ext == 'xlsx':
        df.to_excel(buffer, index=False)
    elif ext == 'tsv':
        df.to_csv(buffer, index=False, sep='\t')
    else:
        raise('Only "csv", "xlsx" and "tsv" extensions are accepted')
    
    type = mimetypes.guess_type(f'_.{ext}')[0]
    
    return FileStorage(
        stream=open(buffer.name, 'rb'),
        filename=f'test.{ext}',
        content_type=type,
    )
    
def df_2_json(df:pd.DataFrame) -> str:  # *
    """Converts from dataframe to JSON string.

    Args:
        df (pd.DataFrame): Data.

    Returns:
        str: JSON string data.
    """
    return json.dumps(df.to_numpy().tolist())

def z_norm(df:pd.DataFrame) -> pd.DataFrame:
    """Normalized dataframe to a mean of 0 and standard deviation of 1.

    Args:
        df (pd.DataFrame): Data to transform.

    Returns:
        pd.DataFrame: Normalized data.
    """
    return (df - df.mean())/df.std()

def compare(inner_df:pd.DataFrame, outer_df:pd.DataFrame, inner_column:str, outer_column:str,
            find_same:bool=True, combine_headers:bool=False) -> pd.DataFrame:
    """Compares two DataFrames along two specified column names.

    Args:
        inner_df (pd.DataFrame): Data to search for in outer_df.
        outer_df (pd.DataFrame): Data to query with inner_df.
        inner_column (str): Name of column to compare along in inner_df.
        outer_column (str): Name of column to compare along in outer_df.
        find_same (bool, optional): If True returns same values, if False returns values in outer_df column not found in
            inner_df column. Defaults to True.
        combine_headers (bool, optional): If True, returns a DataFrame with both inner_df and outer_df headers.
            Defaults to False.

    Returns:
        pd.DataFrame: outer_df with condition specified by find_same.
    """
    outer_in_inner = outer_df[outer_column].isin(inner_df[inner_column])
    indices = outer_in_inner[(outer_in_inner if find_same else ~outer_in_inner)].index
    
    if combine_headers and find_same:
        inner_df_compare = compare(inner_df=outer_df,  # Swap outer w/ inner
                                   outer_df=inner_df,
                                   inner_column=outer_column,
                                   outer_column=inner_column,
                                   find_same=True,  # Only for shared
                                   combine_headers=False)  # Don't run again (infinitely)
        
        return pd.merge(outer_df.iloc[indices], inner_df_compare, how='left', left_on=outer_column, right_on=inner_column)
        
    return outer_df.iloc[indices]

def concat(dfs:Iterable[pd.DataFrame], drop_uncommon_columns:bool=True) -> pd.DataFrame:
    """Wrapper for pd.concat. Stacks DataFrames and sorts.

    Args:
        dfs (Iterable[pd.DataFrame]): Collection of DataFrames.
        drop_uncommon_columns (bool, optional): Determines pd join method. Defaults to True.

    Returns:
        pd.DataFrame: Concatenated data.
    """
    return pd.concat(dfs, axis=0, ignore_index=True, join=('inner' if drop_uncommon_columns else 'outer'), sort=True)

def sync_na_drop(df:Union[pd.DataFrame, pd.Series], col_s:Union[str, List[str]], *iterables:Iterable,
                 all_na:bool=True) -> Tuple[pd.DataFrame, Union[list, List[list]]]:
    """Syncs NaN values in a dataframe with a list of iterables.

    Args:
        df (pd.DataFrame): Data to drop from.
        col_s (Union[str, list]): Name of single column or list of columns to subset for drop.
        all_na (bool): True, drops row only if all values in row are NaN. Else drops row if any values is NaN.
        Defaults to True.

    Returns:
        Tuple[List[Iterable], pd.DataFrame]: Tuple of list of masked iterables and NA dropped DataFrame.
    """
    if not all(len(i) == len(df) for i in iterables):
        raise ValueError('All iterables must be the same length as the dataframe.')
     
    f = df[col_s].isnull
    if isinstance(df[col_s], pd.DataFrame):
        is_na_mask = f().all(axis=1) if all_na else f().any(axis=1)
    elif isinstance(df[col_s], pd.Series):
        is_na_mask = f()
    
    if len(iterables) == 1:
        out = np.array(iterables[0])[~is_na_mask].tolist()
    else:
        out = [np.array(it)[~is_na_mask].tolist() for it in iterables]

    subset = list(col_s) if not isinstance(col_s, str) else [col_s]
    return (df.dropna(subset=subset, how=('all' if all_na else 'any')),
            out)
