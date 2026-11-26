"""
Ex-09: AQI Time Series Analysis (Tucson, AZ — 2022)

Goal:
- Explore AQI time series for patterns (trend + seasonality)
- Test stationarity (ADF)
- Fit ARIMA via auto_arima
- Forecast future AQI
- Detrend and examine seasonality in detrended series

Dataset:
- data/ad_aqi_tracker_data-2023.csv
  (You will clean column names and coerce types.)

Your job in this file:
- Implement the TODO sections.
- Keep functions small and testable.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

from pmdarima import auto_arima


# ---------------------------------------------------------------------
# Step 1: Load + Preprocess
# ---------------------------------------------------------------------

def load_aqi(path: str = "data/ad_aqi_tracker_data-2023.csv") -> pd.DataFrame:
    """
    Load the AQI dataset and standardize column names.

    TODO:
    - Read CSV into a DataFrame
    - Standardize/clean column names to snake_case
      (Hint: minimally: strip, lower, replace spaces with underscores)
    - Convert placeholder missing values (e.g., '.' or '') to NaN
    - Drop rows with missing date or aqi_value
    - Ensure you end up with columns:
        - date (datetime)
        - aqi_value (numeric)

    Return
    ------
    df : pd.DataFrame
        Indexed by datetime 'date' and sorted.
    """
    # df = pd.read_csv(path)
    # TODO: clean column names
    # TODO: rename columns if needed (e.g., "date" vs "date_" or "aqi_values")
    # TODO: coerce types and drop NA
    # TODO: set index to date and sort
    raise NotImplementedError("Complete load_aqi() TODOs.")


def plot_series(df: pd.DataFrame, col: str = "aqi_value", title: str = "AQI Time Series"):
    """
    Plot the AQI time series.

    TODO:
    - Create a labeled plot
    - Use df.index as x-axis
    """
    # df[col].plot(...)
    # plt.title(...)
    # plt.ylabel(...)
    # plt.show()
    raise NotImplementedError("Complete plot_series() TODOs.")


# ---------------------------------------------------------------------
# Step 2: Decomposition (trend/seasonal/resid)
# ---------------------------------------------------------------------

def decompose_series(series: pd.Series, period: int = 7, model: str = "additive"):
    """
    Decompose a time series into trend/seasonal/residual components.

    Parameters
    ----------
    series : pd.Series
        AQI series indexed by datetime.
    period : int
        Seasonal period. Daily data often uses:
        - 7 for weekly seasonality
        - ~365 for yearly seasonality (may be too large for short series)
    model : str
        'additive' or 'multiplicative'

    TODO:
    - Call seasonal_decompose with the chosen model and period

    Return
    ------
    decomposition : DecomposeResult
    """
    # decomposition = seasonal_decompose(series, model=model, period=period)
    # return decomposition
    raise NotImplementedError("Complete decompose_series() TODOs.")


def plot_decomposition(decomposition):
    """
    Plot decomposition output.

    TODO:
    - Call decomposition.plot()
    - plt.show()
    """
    raise NotImplementedError("Complete plot_decomposition() TODOs.")


# ---------------------------------------------------------------------
# Step 3: Stationarity Testing + Differencing
# ---------------------------------------------------------------------

def adf_test(series: pd.Series):
    """
    Run Augmented Dickey-Fuller test.

    TODO:
    - Call adfuller(series)
    - Return a dict with:
        - adf_stat
        - p_value
        - n_lags
        - n_obs
        - critical_values (dict)

    Hint: print statements are fine for exploration, but tests (if any)
    usually prefer returned values.
    """
    raise NotImplementedError("Complete adf_test() TODOs.")


def difference(series: pd.Series, d: int = 1) -> pd.Series:
    """
    Apply differencing d times.

    TODO:
    - Iteratively difference using .diff()
    - Drop missing values created by differencing
    """
    raise NotImplementedError("Complete difference() TODOs.")


# ---------------------------------------------------------------------
# Step 4: ARIMA (auto_arima) + In-sample fit
# ---------------------------------------------------------------------

def fit_auto_arima(
    series: pd.Series,
    start_p: int = 1,
    start_q: int = 1,
    max_p: int = 3,
    max_q: int = 3,
    seasonal: bool = False,
    m: int = 1,
    random_state: int = 42,
):
    """
    Fit an ARIMA model using pmdarima.auto_arima to select (p,d,q).

    TODO:
    - Call auto_arima with reasonable settings:
        - test='adf'
        - d=None
        - seasonal=False by default (you can discuss seasonality separately)
        - suppress_warnings=True
        - error_action='ignore'
        - stepwise=True
    - Fit the returned model to the series (auto_arima returns a fitted model)
    - Return the fitted model
    """
    raise NotImplementedError("Complete fit_auto_arima() TODOs.")


def add_fitted_values(df: pd.DataFrame, model, col: str = "aqi_value") -> pd.DataFrame:
    """
    Add in-sample fitted values to df.

    TODO:
    - Create a new column 'fitted' with model.predict_in_sample()
    - Return a copy of df with 'fitted'
    """
    raise NotImplementedError("Complete add_fitted_values() TODOs.")


def plot_fitted(df: pd.DataFrame, actual_col: str = "aqi_value", fitted_col: str = "fitted"):
    """
    Plot original vs fitted values.

    TODO:
    - Plot both series on the same axes with labels
    """
    raise NotImplementedError("Complete plot_fitted() TODOs.")


# ---------------------------------------------------------------------
# Step 5: Forecasting
# ---------------------------------------------------------------------

def forecast_next(model, last_date: pd.Timestamp, periods: int = 30, freq: str = "D"):
    """
    Forecast future values.

    TODO:
    - Use model.predict(n_periods=periods, return_conf_int=True)
    - Build a future DatetimeIndex starting the day AFTER last_date
    - Return (future_index, forecast, conf_int)

    Notes:
    - conf_int should be a (periods, 2) array
    """
    raise NotImplementedError("Complete forecast_next() TODOs.")


def plot_forecast(
    df: pd.DataFrame,
    future_index: pd.DatetimeIndex,
    forecast: np.ndarray,
    conf_int: np.ndarray,
    col: str = "aqi_value",
    title: str = "AQI Forecast",
):
    """
    Plot historical AQI with forecast and confidence interval.

    TODO:
    - Plot historical series
    - Plot forecast series
    - Fill between conf_int bounds
    - Add labels/legend/title
    """
    raise NotImplementedError("Complete plot_forecast() TODOs.")


# ---------------------------------------------------------------------
# Step 6: Detrending + Seasonality Checks
# ---------------------------------------------------------------------

def detrend_moving_average(series: pd.Series, window: int = 12) -> pd.Series:
    """
    Detrend by subtracting a rolling mean.

    TODO:
    - Compute rolling mean with the given window
    - Subtract it from original series
    - Drop NA values created by rolling
    """
    raise NotImplementedError("Complete detrend_moving_average() TODOs.")


def monthly_seasonality_summary(series: pd.Series) -> pd.DataFrame:
    """
    Simple seasonality summary: average value by month.

    TODO:
    - Group by series.index.month (or series.index.to_period('M').month)
    - Compute mean and count
    - Return a DataFrame sorted by month with columns: month, mean, n
    """
    raise NotImplementedError("Complete monthly_seasonality_summary() TODOs.")

