#! /usr/bin/env python

import pandas as pd
import numpy as np
import statsmodels.api as sm
# from datetime import datetime
from dateutil.relativedelta import relativedelta


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

    def seasonal(self, org_df, key='mf', forecast=False):
        """ Attempts to fit a seasonal ARIMAX model to a column (key) in a dataframe.  If the
            fit is successful, estimate a 12 month forecast and use the fit and forecast
            to create a "gap filled" version of the data.
        """

        df = org_df.copy()

        # first and last good points (skips over nans)
        pt0 = df[key].first_valid_index()
        pt1 = df[key].last_valid_index()
        # find the column name of the 'sd' data.
        sdkey = [s for s in df.columns if 'sd' in s]

        """ seasonal ARIMAX model
            Will only work on monthly data.  I could add a check to make sure
            the data is at the correct rate...
        """
        # force df.index to be inferred to prevent statsmodel warning (GSD 200226)
        df.index = pd.DatetimeIndex(df.index.values, freq=df.index.inferred_freq)
        mod = sm.tsa.statespace.SARIMAX(df[key][pt0:], order=(1, 1, 0), seasonal_order=(1, 1, 1, 12))

        try:
            results = mod.fit(disp=0)
        except (ValueError, LinAlgError) as e:
            """ This error can occur when the dataset is too short  """
            print(f'SARIMAX failed to fit for {self.site}')
            df['model'] = np.nan
            df['gf'] = df[key]
            df['gf'] = df['gf'][pt0:pt1].interpolate(method='time')
            df['gfsd'] = df[sdkey]
            df['gfsd'] = df.loc[pt0:pt1, sdkey].fillna(df[sdkey].median())
            return df

        # SARIMAX model results
        df['model'] = results.predict(start=pt0+relativedelta(months=16))
        df.loc[pt1+relativedelta(months=1):, 'model'] = np.nan

        # gap fill 'gf' with model data
        df['gf'] = df[key].fillna(df['model'])

        # add 12-month forecast to gf column
        if forecast:
            # 12-month forecast from the last valid measurement
            f = results.predict(start=pt1+relativedelta(months=1), end=pt1+relativedelta(months=13), dynamic=True)
            df = pd.concat([df, f.rename('forecast')], axis=1)
            # if True add forecast data to the end of 'gf'
            # df.loc[pt1:, 'gf'] = df.loc[pt1:, 'forecast']
            # df.drop(['forecast'], axis=1, inplace=True)

        # interpolate any missing data that the "model" doesn't fill in.
        # inplace=True does not work
        df['gf'].update(df.loc[pt0:pt1, 'gf'].interpolate(method='time'))
        # missing gfsd are filled in with median of sd
        df['gfsd'] = df[sdkey].fillna(df[sdkey].median())
        df.loc[:pt0-relativedelta(months=1), 'gfsd'] = np.nan
        df.loc[pt1+relativedelta(months=1):, 'gfsd'] = np.nan
        # need to add forcast error for gfsd

        return df


    def robust_seasonal(self, org_df, key='mf', forecast=False):
        """ This method handles data sets that have many nans in the first 16 months by running
            the SARIMAX model on reverse of the data and then inverting the results. """

        df = self.seasonal(org_df, key=key)
        if df['gf'].max() > df[key].median() + df[key].std()*2:
            # print('inverting data')
            df['invert'] = org_df[key].values[::-1]
            dfi = self.seasonal(df, key='invert')
            df['gf'] = dfi['gf'].values[::-1]
            df.drop(['invert'], inplace=True, axis=1)

        if forecast:
            df2 = self.seasonal(org_df, key=key, forecast=True)
            df = pd.concat([df, df2['forecast']], axis=1)

        return df
