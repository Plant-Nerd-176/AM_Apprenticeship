""" This file contains the modelling functions """

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    explained_variance_score,
    max_error
)
import numpy as np
import pandas as pd

def fit_wsl_linear_model(
    model_df: pd.DataFrame,
    feature_cols: list,
    target_col: str = 'Attendance',
    split_year: int = 2022,
    forecast_years: int = 0
):
    """
    Fit a linear regression model to WSL attendance data.
    
    Args:
        model_df (pd.DataFrame): DataFrame containing the modelling data.
        feature_cols (list): List of feature column names.
        target_col (str): Name of the target column. Default is 'Attendance'.
        split_year (int): Year to split train/test data. Default is 2022.
        forecast_years (int): Number of future years to forecast. Default is 0.
        
    Returns:
        dict: A dictionary containing the fitted model, feature columns,
              train/test DataFrames with predictions, future forecasts,
              and performance metrics DataFrames. 
    """

    # Ensure Season is NOT in feature columns
    feature_cols = [c for c in feature_cols if c != 'Season']

    # Train/test split
    train_df = model_df[model_df['Season'] < split_year].copy()
    test_df  = model_df[model_df['Season'] >= split_year].copy()

    X_train = train_df[feature_cols]
    y_train = train_df[target_col]

    X_test = test_df[feature_cols]
    y_test = test_df[target_col]
    
    # Fit model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    train_df['Predicted_Attendance'] = model.predict(X_train)
    test_df['Predicted_Attendance']  = model.predict(X_test)

    # Future forecasting (pattern-based per club)
    future_df = None
    if forecast_years > 0:

        last_year = model_df['Season'].max()
        future_years_list = list(range(last_year + 1, last_year + 1 + forecast_years))

        club_cols = [c for c in model_df.columns if c.startswith('Club_')]
        clubs = [c.replace('Club_', '') for c in club_cols]

        future_rows = []

        for club in clubs:

            # Historical rows for this club
            cdf = model_df[model_df[f'Club_{club}'] == 1].sort_values('Season')


            # If club only appears once, cannot compute growth
            if len(cdf) < 2:
                for year in future_years_list:
                    row = {'Season': year, 'Club': club}

                    # Dummy columns
                    for c in club_cols:
                        row[c] = 1 if c == f'Club_{club}' else 0

                    # Capacity = last known or NaN
                    row['Capacity'] = (
                        cdf['Capacity'].iloc[-1]
                        if 'Capacity' in cdf.columns else np.nan
                    )

                    # No predictions for non-regular clubs
                    row['Predicted_Attendance'] = np.nan
                    row[target_col] = np.nan

                    # All feature columns = NaN
                    for col in feature_cols:
                        row[col] = np.nan

                    future_rows.append(row)

                continue  # Skip forecasting logic

            # Normal forecasting for regular clubs
            # Compute year-to-year growth in attendance
            cdf['growth'] = cdf[target_col].pct_change()

            # Use median growth (robust)
            median_growth = cdf['growth'].median()

            # Last known attendance
            last_att = cdf[target_col].iloc[-1]

            # Last known feature values
            last_row = cdf.iloc[-1]

            for year in future_years_list:

                # Apply growth pattern
                last_att = last_att * (1 + median_growth)

                row = {'Season': year}

                # Carry forward feature values
                for col in feature_cols:
                    row[col] = last_row[col]

                # Dummy columns
                for c in club_cols:
                    row[c] = 1 if c == f'Club_{club}' else 0

                # Capacity stays the same
                row['Capacity'] = last_row['Capacity']

                # Club name
                row['Club'] = club

                # Forecasted attendance
                row['Predicted_Attendance'] = last_att

                # No actual attendance
                row[target_col] = np.nan

                future_rows.append(row)

        future_df = pd.DataFrame(future_rows)

    # Metrics
    def compute_metrics(y_true, y_pred):
        return {
            'MAE': mean_absolute_error(y_true, y_pred),
            'MSE': mean_squared_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'R2': r2_score(y_true, y_pred),
            'ExplainedVariance': explained_variance_score(y_true, y_pred),
            'MaxError': max_error(y_true, y_pred),
            'PctWithin10pct': np.mean(np.abs((y_true - y_pred) / y_true) <= 0.10),
            'PctWithin15pct': np.mean(np.abs((y_true - y_pred) / y_true) <= 0.15),
            'PctWithin500Attendees': np.mean(np.abs(y_true - y_pred) <= 500),
            'PctWithin1000Attendees': np.mean(np.abs(y_true - y_pred) <= 1000)
        }

    train_metrics_df = pd.DataFrame(
        compute_metrics(y_train, train_df['Predicted_Attendance']), index=['Train']
    )
    test_metrics_df = pd.DataFrame(
        compute_metrics(y_test, test_df['Predicted_Attendance']), index=['Test']
    )
    combined_metrics_df = pd.concat([train_metrics_df, test_metrics_df])

    # Datatype enforcement
    int_cols = [
        'Matches', 'Wins', 'Draws', 'Losses',
        'Goals_For', 'Goals_Against', 'Goal_Difference',
        'Points', 'Top_Scorer_Goals',
        'Eng_Num_Players', 'FIFA_Ranking',
        'Capacity', 'years_since_euro'
    ]

    def enforce_types(df):
        if df is None:
            return None

        # Cast integer columns
        for col in int_cols:
            if col in df.columns:
                df[col] = df[col].round().astype('Int64')

        # Round everything else to 2dp
        df = df.round(2)

        return df

    train_df = enforce_types(train_df)
    test_df = enforce_types(test_df)
    future_df = enforce_types(future_df)

    # Results
    return {
        'model': model,
        'features': feature_cols,
        'train_df': train_df,
        'test_df': test_df,
        'future_df': future_df,
        'train_metrics_df': train_metrics_df,
        'test_metrics_df': test_metrics_df,
        'combined_metrics_df': combined_metrics_df
    }

