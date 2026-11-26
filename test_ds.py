import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pytest
import ds


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------

@pytest.fixture(scope="session")
def df():
    return ds.load_aqi("data/ad_aqi_tracker_data-2023.csv")


@pytest.fixture(scope="session")
def series(df):
    assert "aqi_value" in df.columns
    s = df["aqi_value"]
    # Ensure no NAs for modeling functions
    s = pd.to_numeric(s, errors="coerce").dropna()
    return s


# ---------------------------------------------------------------------
# Step 1: Load + Preprocess
# ---------------------------------------------------------------------

def test_load_aqi_returns_dataframe(df):
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_aqi_has_datetime_index(df):
    assert isinstance(df.index, pd.DatetimeIndex), "Index must be DatetimeIndex"
    assert df.index.is_monotonic_increasing, "Index should be sorted ascending"


def test_load_aqi_has_required_column(df):
    assert "aqi_value" in df.columns, "DataFrame must contain 'aqi_value'"


def test_aqi_value_is_numeric_and_nonmissing(df):
    s = pd.to_numeric(df["aqi_value"], errors="coerce")
    assert s.notna().all(), "aqi_value should be numeric after preprocessing (no NaNs)"
    assert (s >= 0).all(), "AQI values should be non-negative"


def test_plot_series_runs(df):
    ds.plot_series(df, col="aqi_value", title="AQI Time Series (Test)")
    plt.close("all")


# ---------------------------------------------------------------------
# Step 2: Decomposition
# ---------------------------------------------------------------------

def test_decompose_series_returns_components(series):
    # Use small period to avoid requiring long seasonal cycles
    decomposition = ds.decompose_series(series, period=7, model="additive")

    # DecomposeResult typically has these attributes:
    for attr in ["trend", "seasonal", "resid"]:
        assert hasattr(decomposition, attr), f"Decomposition missing '{attr}'"


def test_plot_decomposition_runs(series):
    decomposition = ds.decompose_series(series, period=7, model="additive")
    ds.plot_decomposition(decomposition)
    plt.close("all")


# ---------------------------------------------------------------------
# Step 3: Stationarity + Differencing
# ---------------------------------------------------------------------

def test_adf_test_returns_expected_dict(series):
    out = ds.adf_test(series)

    assert isinstance(out, dict), "adf_test must return a dict"
    for key in ["adf_stat", "p_value", "n_lags", "n_obs", "critical_values"]:
        assert key in out, f"adf_test output missing '{key}'"

    assert np.isfinite(out["adf_stat"]), "ADF statistic must be finite"
    assert 0.0 <= float(out["p_value"]) <= 1.0, "p_value must be in [0, 1]"
    assert isinstance(out["critical_values"], dict), "critical_values must be a dict"


def test_difference_d1(series):
    d1 = ds.difference(series, d=1)
    assert isinstance(d1, pd.Series)
    assert len(d1) < len(series), "Differencing should reduce series length"
    assert d1.notna().all(), "Differenced series should not contain NaNs"


def test_difference_d2(series):
    d2 = ds.difference(series, d=2)
    assert isinstance(d2, pd.Series)
    assert len(d2) < len(series), "Differencing twice should reduce series length"
    assert d2.notna().all(), "Differenced series should not contain NaNs"


# ---------------------------------------------------------------------
# Step 4: ARIMA Fit + In-sample fitted
# ---------------------------------------------------------------------

def test_fit_auto_arima_returns_model(series):
    model = ds.fit_auto_arima(
        series,
        start_p=1, start_q=1, max_p=3, max_q=3,
        seasonal=False, m=1
    )
    # pmdarima ARIMA usually has these methods
    assert hasattr(model, "predict_in_sample"), "Model must support predict_in_sample()"
    assert hasattr(model, "predict"), "Model must support predict()"


def test_add_fitted_values_adds_column(df, series):
    model = ds.fit_auto_arima(series, seasonal=False, m=1)
    out = ds.add_fitted_values(df, model, col="aqi_value")

    assert isinstance(out, pd.DataFrame)
    assert "fitted" in out.columns, "add_fitted_values must add a 'fitted' column"

    fitted = pd.to_numeric(out["fitted"], errors="coerce")
    assert fitted.notna().all(), "fitted values must be numeric and non-missing"
    assert len(fitted) == len(out), "fitted length must match df length"


def test_plot_fitted_runs(df, series):
    model = ds.fit_auto_arima(series, seasonal=False, m=1)
    out = ds.add_fitted_values(df, model, col="aqi_value")
    ds.plot_fitted(out, actual_col="aqi_value", fitted_col="fitted")
    plt.close("all")


# ---------------------------------------------------------------------
# Step 5: Forecasting
# ---------------------------------------------------------------------

def test_forecast_next_shapes(series, df):
    model = ds.fit_auto_arima(series, seasonal=False, m=1)
    last_date = df.index.max()

    future_index, forecast, conf_int = ds.forecast_next(
        model, last_date=last_date, periods=30, freq="D"
    )

    assert isinstance(future_index, pd.DatetimeIndex)
    assert len(future_index) == 30, "future_index must have length == periods"
    assert len(forecast) == 30, "forecast must have length == periods"

    conf_int = np.asarray(conf_int)
    assert conf_int.shape == (30, 2), "conf_int must have shape (periods, 2)"

    # index should start AFTER last_date
    assert future_index.min() > last_date, "future_index must start after last_date"


def test_plot_forecast_runs(series, df):
    model = ds.fit_auto_arima(series, seasonal=False, m=1)
    last_date = df.index.max()

    future_index, forecast, conf_int = ds.forecast_next(
        model, last_date=last_date, periods=30, freq="D"
    )

    ds.plot_forecast(df, future_index, forecast, conf_int, col="aqi_value", title="Forecast Test")
    plt.close("all")


# ---------------------------------------------------------------------
# Step 6: Detrending + Seasonality
# ---------------------------------------------------------------------

def test_detrend_moving_average(series):
    det = ds.detrend_moving_average(series, window=12)
    assert isinstance(det, pd.Series)
    assert len(det) < len(series), "Rolling detrend should shorten series (drops initial window NaNs)"
    assert det.notna().all(), "Detrended series should not contain NaNs"


def test_monthly_seasonality_summary(series):
    # Ensure datetime index exists (it should from load_aqi)
    assert isinstance(series.index, pd.DatetimeIndex)

    summary = ds.monthly_seasonality_summary(series)

    assert isinstance(summary, pd.DataFrame)
    for col in ["month", "mean", "n"]:
        assert col in summary.columns, f"Summary missing '{col}'"

    assert summary["month"].between(1, 12).all(), "Months must be 1..12"
    assert (summary["n"] > 0).all(), "Each month should have at least 1 observation"
    assert np.isfinite(summary["mean"]).all(), "Means must be finite"
