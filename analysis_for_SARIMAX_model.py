import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

data = pd.read_csv('Value Data 1.csv')

# Convert Unix timestamps to datetime
data['Time'] = pd.to_datetime(data['Time (Unix)'], unit='s')
data.set_index('Time', inplace=True)
print(data.head())

# Extract the series
series = data['Value']

# --- analysis
# - visulize the original data
plt.figure(figsize=(14, 7))
plt.plot(series, label='Original Data')
plt.title('Time Series Data')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()

# - Decompose the series into trend, seasonal, and residual components
decomposition = seasonal_decompose(series, model='additive', period=1440)
fig = decomposition.plot()
fig.set_size_inches(14, 8)
plt.show()

# - Check stationarity with the Augmented Dickey-Fuller test
adf_test = adfuller(series)
print(f"ADF Statistic: {adf_test[0]}")
print(f"p-value: {adf_test[1]}")

if adf_test[1] > 0.05:
    print("Series is not stationary. Differencing is needed.")
    # Differencing the series to make it stationary
    series_diff = series.diff().dropna()
else:
    print("Series is stationary.")
    series_diff = series

# - Plot ACF and PACF to determine the order of AR and MA components
fig, ax = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(series_diff, ax=ax[0])
plot_pacf(series_diff, ax=ax[1])
plt.show()