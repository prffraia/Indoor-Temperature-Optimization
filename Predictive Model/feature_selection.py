import numpy as np
import pandas as pd

from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import roll_time_series

from statsmodels.tsa.stattools import adfuller

from sklearn.preprocessing import StandardScaler

def check_stationarity(df, threshold=0.05, max_diff=1):
    """
    Function to check stationarity of each column in a DataFrame using the Augmented Dickey-Fuller (ADF) test,
    and apply differencing until the series becomes stationary or the maximum number of differences is reached.

    Parameters:
    - df: pandas DataFrame containing the rolled data. Note that the df must have timestamp as index and target variable must be in index 0!
    - threshold: Threshold value for p-value to determine stationarity (default is 0.05).
    - max_diff: Maximum number of differencing steps allowed (default is 2).

    Returns:
    - df_stationary: DataFrame with stationary columns.
    """
    df_stationary = pd.DataFrame(index=df.index)


    for col in df.columns:
        series = df[col]
        diff_count = 0
        p_value = 1  # Initialize p-value to start the loop

        while p_value > threshold and diff_count < max_diff:
            adf_result = adfuller(series.values.flatten())
            print(col)
            print('ADF Statistic: %f' % adf_result[0])
            print('p-value: %f' % adf_result[1])
            print("\n")
            p_value = adf_result[1]

            if p_value > threshold:
                series = series.diff().dropna()  # Difference the series
                diff_count += 1
            elif p_value < threshold:
               df_stationary[col] = series

    return df_stationary

def scaling(df):

    scaler = StandardScaler()
    df_scaler = scaler.fit(df)
    df_scaled = df_scaler.transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns = df.columns, index = df.index)
    return df_scaled, scaler

def feat_extraction(df, target_col):
    """
    Function to extract features and preprocess for feature selection
    
    Parameters:
    - df: df after stationarity conversion. The index must be reset to be compatible with tsfresh.extract_features() function

    Returns:
    - X_extracted_features: DataFrame with extracted features without NA's
    """
    df.dropna(inplace = True)
    y = df[target_col]
    df.reset_index(inplace = True)

    #extract features from all the varaibles except the target varaible
    features = extract_features(df.loc[:, df.columns != target_col], column_id="timestamp", column_sort="timestamp")

    # Drop all columns with NAN's
    X = features
    X = X.dropna(axis=1, how="any")

    return X, y

def feat_selection(X, y):
    """
    Function for feature selection 
    
    Parameters:
    - df: df after stationarity conversion. The index must be reset to be compatible with tsfresh.extract_features() function

    Returns:
    - X_"""
    df_y = pd.DataFrame(y)
    df_y = df_y.set_index(X.index)
    y = df_y.iloc[:, 0]

    # Feature Selection
    selection = select_features(X, y, fdr_level=0.01)

    return selection


def feat_engineering(df, target_col, threshold = 0.05, max_diff = 2):
  """
  Function that performs feature engineering pipeline for time series data.

  Parameters:
      df: pandas DataFrame containing the data (timestamp as index).
      target_col: Index of the target variable column in the DataFrame (default is 0).

  Returns:
      selected_features: List of selected features after feature selection.
  """
  df_stationary = check_stationarity(df)
  df_scaled, scaler = scaling(df_stationary)
  X, y = feat_extraction(df_scaled, target_col)

  # Feature Selection (consider exploring different methods)
  selection = feat_selection(X, y)

  return selection, y, scaler