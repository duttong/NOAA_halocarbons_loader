#! /usr/bin/env python

""" Improved seasonal gap-filling methods for time series data. 2025-06-17 """

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class Gap_Methods:

    def linear(self, org_df, key='mf'):
        """ Linear interpolation """

        df = org_df.copy()

        # first and last good points (skips over nans)
        pt0 = df[key].first_valid_index()
        pt1 = df[key].last_valid_index()
        # find the column name of the 'sd' data.
        sdkey = [s for s in df.columns if 'sd' in s]

        df['gf'] = df[key]
        df['gf'] = df['gf'][pt0:pt1].interpolate(method='time')
        df['gfsd'] = df[sdkey]
        df['gfsd'] = df.loc[pt0:pt1, sdkey].fillna(df[sdkey].median())

        return df

    def seasonal(self, df, col='mf', freq='MS', seasonal_periods=12, forecast_periods=0):
        """
        Fill gaps and optionally forecast future values with additive Holt–Winters.

        Parameters
        ----------
        df : pandas.DataFrame
            Must have a DatetimeIndex and a column named `col`.
        col : str, default 'mf'
            The name of the series to gap-fill.
        freq : str, default 'MS'
            Frequency for the full index (e.g. 'MS' for month-start).
        seasonal_periods : int, default 12
            The length of the seasonal cycle (12 for monthly data).
        forecast_periods : int, default 0
            Number of periods (in same freq) to forecast beyond the last date.

        Returns
        -------
        pandas.DataFrame
            Indexed from the first date to last+forecast; columns:
            - col          : original series (NaN for forecast dates)
            - f'{col}_hw'  : Holt–Winters fitted + forecast values
            - f'{col}_filled': original where present, HW fill where missing
        """
        # 1. Original series
        ts = df[col]
        #start, last = ts.index.min(), ts.index.max()
        start = ts.first_valid_index()
        last  = ts.last_valid_index()

        # 2. Extended index (includes forecast)
        end = last + pd.DateOffset(months=forecast_periods) if forecast_periods > 0 else last
        full_idx = pd.date_range(start, end, freq=freq)

        # 3. Training series (only through last)
        train_idx = pd.date_range(start, last, freq=freq)
        ts_train_full = ts.reindex(train_idx)
        ts_train = ts_train_full.interpolate(method='time')

        # 4. Fit Holt–Winters with estimated initialization
        hw = ExponentialSmoothing(
            ts_train,
            trend='add',
            seasonal='add',
            seasonal_periods=seasonal_periods,
            initialization_method='estimated'
        ).fit(optimized=True)

        # 5. Predict over full span (including future)
        hw_pred = hw.predict(start=full_idx[0], end=full_idx[-1])

        # 6. Assemble output DataFrame
        out = pd.DataFrame({
            col: ts.reindex(full_idx),
            f'{col}_mod': hw_pred
        }, index=full_idx)
        out[f'{col}_filled'] = out[col].fillna(out[f'{col}_mod'])

        return out
