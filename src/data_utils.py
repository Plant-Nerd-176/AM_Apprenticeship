""" This file contains functions for data processing."""

import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------------
# Data Import
# -------------------------------------------------------------------------
def load_csv_data(
        file_path: str
) -> pd.DataFrame:
    """Load data from a CSV file into a pandas DataFrame.
    Args:
        file_path (str): Path to the CSV file.
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    path = Path(file_path)

    if not path.exists():
        print(f"CSV file not found: {file_path}")
        return None   
    
    df = pd.read_csv(path)
    return df

# -------------------------------------------------------------------------
# Data Cleaning and Transformation
# -------------------------------------------------------------------------
def remove_string_parts(df: pd.DataFrame, column: str, substring: str) -> pd.DataFrame:
    """Remove a specified substring from a given column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column to clean.
        substring (str): The substring to remove.

    Returns:
        pd.DataFrame: DataFrame with cleaned column.
    """
    df[column] = df[column].astype(str).str.replace(substring, "", regex=False)
    return df


def convert_column_names(df: pd.DataFrame, columns_map: dict) -> pd.DataFrame:
    """Rename columns based on a mapping dictionary.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns_map (dict): Mapping of {old_name: new_name}.

    Returns:
        pd.DataFrame: DataFrame with renamed columns.
    """
    return df.rename(columns=columns_map)


def create_unique_id(df: pd.DataFrame, columns: list, new_column: str) -> pd.DataFrame:
    """Create a unique identifier by concatenating specified columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (list): Columns to concatenate.
        new_column (str): Name of the new ID column.

    Returns:
        pd.DataFrame: DataFrame with added unique ID column.
    """
    df[new_column] = df[columns].astype(str).agg("_".join, axis=1)
    return df


def split_column(df: pd.DataFrame, column: str, separator: str, new_columns: list) -> pd.DataFrame:
    """Split a column into multiple columns using a separator.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column to split.
        separator (str): Separator character.
        new_columns (list): Names of new split columns.

    Returns:
        pd.DataFrame: DataFrame with new split columns.
    """
    split_data = df[column].astype(str).str.split(separator, expand=True)

    for i, new_col in enumerate(new_columns):
        df[new_col] = split_data[i] if i in split_data.columns else None

    return df


def map_values(df: pd.DataFrame, column: str, mapping_dict: dict) -> pd.DataFrame:
    """Map categorical values in a column to new values.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column to map.
        mapping_dict (dict): Mapping of {old_value: new_value}.

    Returns:
        pd.DataFrame: DataFrame with updated values.
    """
    df[column] = df[column].map(mapping_dict).fillna(df[column])
    return df


def convert_to_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Drop specified columns from the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (list): List of columns to drop.

    Returns:
        pd.DataFrame: DataFrame with specified columns dropped.
    """
    return df.drop(columns=columns, errors="ignore")