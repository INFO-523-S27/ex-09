# Ex-09: Analyzing AQI Time Series with ARIMA

## Objective

In this exercise, you will analyze **Air Quality Index (AQI)** time series data to identify **patterns, trends, and seasonality**, and apply **ARIMA models** to forecast future AQI values.

Beyond fitting a forecasting model, this exercise emphasizes:

* Understanding **time series components** (trend, seasonality, residuals)
* Testing and achieving **stationarity**
* Interpreting **model behavior and forecasts**
* Reasoning about **detrending and seasonal structure** in real-world environmental data

By the end of this exercise, you should be able to explain *how* and *why* an ARIMA model behaves the way it does—rather than treating it as a black box.

---

## Prerequisites

You should have:

* Python 3.9+
* GitHub access
* Familiarity with:

  * pandas and numpy
  * basic time series plots
  * regression concepts
  * train/test ideas (conceptually, even though ARIMA is fit to a single series)

Required libraries (installed via `requirements.txt`):

* `pandas`
* `numpy`
* `matplotlib`
* `statsmodels`
* `pmdarima`

> ⚠️ You do **not** need to create or submit a Jupyter notebook for this exercise.

---

## Dataset

This exercise uses **EPA air quality data** for the **Tucson, AZ Core-Based Statistical Area (CBSA)** for **2022**.

You will work with the dataset:

* **`ad_aqi_tracker_data-2023.csv`**

The data include **daily AQI measurements**, along with contextual information about the monitoring site and primary pollutant.

AQI is a standardized index used by the EPA to communicate how polluted the air currently is and how polluted it is forecast to become.

More information:

* AQI basics: [https://www.airnow.gov/aqi/aqi-basics/](https://www.airnow.gov/aqi/aqi-basics/)

---

## Metadata

| Variable         | Type      | Description               |
| ---------------- | --------- | ------------------------- |
| `date`           | datetime  | Date of observation       |
| `aqi_value`      | int       | Air Quality Index reading |
| `main_pollutant` | character | Primary pollutant         |
| `site_name`      | character | Monitoring site name      |
| `site_id`        | character | Site identifier           |
| `source`         | character | Data source               |

> ⚠️ **Note:** Some columns will require cleaning and type conversion before analysis.

---

## Research Question

> **How can we apply ARIMA modeling to forecast future AQI values based on historical data, and what insights can be gained from detrending and seasonality analysis?**

More specifically:

* Does the AQI series exhibit a clear trend?
* Is there evidence of seasonal patterns (weekly or yearly)?
* How does differencing change the behavior of the series?
* What do ARIMA forecasts suggest about near-term air quality?

---

## Step 1: Setup and Data Preprocessing

You will:

1. Load the AQI dataset from the `data/` directory
2. Clean and standardize column names
3. Convert the date column to datetime and set it as the index
4. Ensure `aqi_value` is numeric and free of missing values
5. Plot the AQI time series for an initial visual inspection

---

## Step 2: Time Series Decomposition

You will:

* Decompose the AQI time series into:

  * **Trend**
  * **Seasonal**
  * **Residual** components
* Use `seasonal_decompose` from `statsmodels`
* Visualize the components to assess underlying structure

> 💡 *Hint:* Daily data often exhibits **weekly seasonality**, but this should be reasoned about rather than assumed.

---

## Step 3: Stationarity and Differencing

You will:

* Perform an **Augmented Dickey-Fuller (ADF)** test to assess stationarity
* Interpret the test statistic and p-value
* Apply **differencing** to the series if necessary
* Re-examine the differenced series

The goal is to understand *why* stationarity matters for ARIMA modeling.

---

## Step 4: ARIMA Modeling

You will:

* Use `auto_arima` from `pmdarima` to select appropriate `(p, d, q)` parameters
* Fit an ARIMA model to the AQI time series
* Examine in-sample fitted values relative to observed AQI

> ⚠️ For this exercise, you should **not** assume seasonal ARIMA (`SARIMA`). Seasonality will be explored separately.

---

## Step 5: Forecasting

You will:

* Forecast AQI values for the **next 30 days**
* Generate confidence intervals for the forecast
* Plot the forecast alongside historical AQI values

Focus on **interpretation**, not just the mechanics of forecasting.

---

## Step 6: Detrending and Seasonality Analysis

You will:

* Apply a **moving average detrending** method
* Analyze the detrended series
* Summarize seasonal behavior (e.g., average AQI by month)

This step helps isolate cyclical behavior from long-term trends.

---

## What You Must Implement

In `ds.py`, you are responsible for implementing:

1. **Data loading and preprocessing**

   * Cleaning columns and indexing by date
2. **Time series visualization**
3. **Seasonal decomposition**
4. **ADF stationarity testing**
5. **Differencing**
6. **ARIMA model fitting**
7. **Forecasting with confidence intervals**
8. **Detrending and seasonality summaries**

Your code must pass the provided **autograder tests**.

---

## Discussion Prompts (Answer in D2L)

In the associated D2L discussion, address the following:

* What trends and seasonal patterns do you observe in the AQI data?
* Was the original series stationary? How did differencing change it?
* How would you describe the short-term AQI forecast produced by the ARIMA model?
* What limitations should be considered when interpreting these forecasts?
* How does detrending help clarify seasonal behavior?

There is no single “correct” answer, but your discussion should reference **your analysis and results**.

---

## Submission Instructions

* Submit **only** your completed `ds.py` file via GitHub
* Do **not** submit notebooks or additional scripts
* Ensure all tests pass before submitting

> The autograder checks **correctness**, **methodology**, and **code quality**.
