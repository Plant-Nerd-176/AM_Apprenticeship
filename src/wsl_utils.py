""" This file contains functions for WSL-specific data processing."""

import pandas as pd

from .data_utils import (
    remove_string_parts,
    convert_column_names,
    create_unique_id,
    convert_to_numeric
)

from config.projects.wsl_config import (
    SEASON_COL_MAP,
    NATIONALITY_COL_MAP,
    EURO_COUNTRIES
)

#--------------------------------------------------------------------------
# WSL-specific Data Cleaning and Transformation
#--------------------------------------------------------------------------
def nationality_group(row):
    """ Assign nationality group based on nationality and euro_flag."""
    if row['Nationality'] == 'England':
        return 'English'
    elif row['euro_flag'] == 1:
        return 'European (excl. Eng)'
    else:
        return 'Non-European'

#-------------------------------------------------------------------------
# WSL Combined Data Processing
#-------------------------------------------------------------------------
def process_wsl_data(
    df: pd.DataFrame,
    start_year: int,
    end_year: int
    ) -> pd.DataFrame:
    """ Process and clean WSL combined data for a given season.
    
    Args:
        df (pd.DataFrame): The input DataFrame to process.
        start_year (int): The starting year of the season.
        end_year (int): The ending year of the season.
    
    Returns:
        pd.DataFrame: The cleaned and processed DataFrame.
    """
    
    if df is None or df.empty:
        print(f'Skipped cleaning for {start_year}_{end_year} (empty or missing)')
        return df

    print(f'Cleaning WSL for season {start_year}_{end_year}...')

    # 1. Remove unwanted string parts
    df = remove_string_parts(df, 'Squad', 'Club Crest ')

    # 2. Normalise club names
    df['Squad'] = df['Squad'].str.replace(' ', '_', regex=False)

    # 3. Add season + unique ID
    df['season'] = f'{start_year}_{end_year}'
    df = create_unique_id(df, ['Squad', 'season'], 'unique_ID')

    # 4. Standardise column names
    df = convert_column_names(df, SEASON_COL_MAP)

    # 5. Handle top_scorer safely
    if 'Top_Scorer' in df.columns:
        split_df = df['Top_Scorer'].str.split(' - ', n=1, expand=True)
        df['Top_Scorer_Name'] = split_df[0]
        df['Top_Scorer_Goals'] = split_df[1] if split_df.shape[1] > 1 else pd.NA

        df = convert_to_numeric(df, ['Top_Scorer_Goals'])

        df['Top_Scorer_Name'] = df['Top_Scorer_Name'].apply(
            lambda x: ', '.join([n.strip().replace(' ', '_') for n in x.split(',')])
            if pd.notna(x) else x
        )
    else:
        print(f"No 'Top_Scorer' column found for {start_year}_{end_year}")
        df['Top_Scorer_Name'] = pd.NA
        df['Top_Scorer_Goals'] = pd.NA

    # 6. Convert numeric columns
    df = convert_to_numeric(df, ['Attendance'])

    print(f'Finished cleaning {start_year}_{end_year} data.')

    return df

#-------------------------------------------------------------------------
# Nationality combined data processing
#-------------------------------------------------------------------------
def process_nationality_data(
    df: pd.DataFrame,
    start_year: int,
    end_year: int
    ) -> pd.DataFrame:  
    """ Process and clean nationality data for a given season.
    
    Args:
        df (pd.DataFrame): The input DataFrame to process.
        start_year (int): The starting year of the season.
        end_year (int): The ending year of the season.  
    
    Returns:
        pd.DataFrame: The cleaned and processed DataFrame.
    """
    
    if df is None or df.empty:
        print(f'Skipped cleaning for {start_year}_{end_year} (empty or missing)')
        return df
    print(f'Cleaning nationality season data for {start_year}_{end_year}...')
    
    # 1. Convert column to string
    df['Nation'] = df['Nation'].astype(str)
    
    # 2. Clean country names
    df['Nation'] = df['Nation'].str.split(' ', n=1).str[1].str.replace(' ', '_', regex=False)

    # 3. Standardise column names
    df = convert_column_names(df, NATIONALITY_COL_MAP)
    
    # 4. Add season + unique ID
    df['season'] = f'{start_year}_{end_year}'
    df = create_unique_id(df,['season', 'Rank'], 'Season_Rank')
        
    # 5. Convert numeric columns
    df = convert_to_numeric(df, ['Num_Players', 'Minutes_Played'])
    
    # 6. Create nationality groups
    df['euro_flag'] = df['Nationality'].apply(lambda x: 1 if x in EURO_COUNTRIES else 0)
    df['group'] = df.apply(nationality_group, axis=1)
    
    print(f'Finished cleaning nationality data for {start_year}_{end_year}.')
    return df
