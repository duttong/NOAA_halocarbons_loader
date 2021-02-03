#! /usr/bin/env python

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime
from dateutil.relativedelta import relativedelta

ftp_path = '/aftp/hats'


class CATS:
    """ CATS instruments """

    def __init__(self):
        self.instrument = 'cats'
        self.sites = ('brw', 'sum', 'nwr', 'mlo', 'smo', 'spo')
        self.rates = ('hourly', 'daily', 'monthly')
        self.molpaths = {
            'F11': f'{ftp_path}/cfcs/cfc11/insituGCs/CATS/',
            'F113': f'{ftp_path}/cfcs/cfc113/insituGCs/CATS/',
            'F12': f'{ftp_path}/cfcs/cfc12/insituGCs/CATS/',
            'N2O': f'{ftp_path}/n2o/insituGCs/CATS/',
            'SF6': f'{ftp_path}/sf6/insituGCs/CATS/',
            'CCl4': f'{ftp_path}/solvents/CCl4/insituGCs/CATS/',
            'MC': f'{ftp_path}/solvents/CH3CCl3/insituGCs/CATS/',
            'h1211': f'{ftp_path}/halons/insituGCs/CATS/',
            'CHCl3': '/home/hats/gdutton/uploads/'}


class RITS:
    """ RITS instruments """

    def __init__(self):
        self.instrument = 'rits'
        self.sites = ('brw', 'mlo', 'nwr', 'smo', 'spo')
        self.molpaths = {
            'F11': f'{ftp_path}/cfcs/cfc11/insituGCs/RITS/',
            'F12': f'{ftp_path}/cfcs/cfc12/insituGCs/RITS/',
            'N2O': f'{ftp_path}/n2o/insituGCs/RITS/',
            'CCl4': f'{ftp_path}/solvents/CCl4/insituGCs/RITS/',
            'MC': f'{ftp_path}/solvents/CH3CCl3/insituGCs/RITS/'}


class Otto:
    """ Otto flask GC """

    def __init__(self):
        self.instrument = 'otto'
        self.sites = ('alt', 'brw', 'cgo', 'hfm', 'itn', 'kum', 'lef', 'mhd', 'mlo',
            'nwr', 'psa', 'smo', 'spo', 'sum', 'thd', 'ush')
        self.molpaths = {
            'F11': f'{ftp_path}/cfcs/cfc11/flasks/Otto/',
            'F113': f'{ftp_path}/cfcs/cfc113/flasks/Otto/',
            'F12': f'{ftp_path}/cfcs/cfc12/flasks/Otto/',
            'N2O': f'{ftp_path}/n2o/flasks/Otto/',
            'SF6': f'{ftp_path}/sf6/flasks/Otto/',
            'CCl4': f'{ftp_path}/solvents/CCl4/flasks/Otto/'}


class OldGC:
    """ Old flask GC, preceeded Otto """

    def __init__(self):
        self.instrument = 'oldgc'
        self.sites = ('alt', 'brw', 'cgo', 'mlo', 'nwr', 'smo', 'spo')
        self.molpaths = {
            'F11': f'{ftp_path}/cfcs/cfc11/flasks/OldGC/',
            'F12': f'{ftp_path}/cfcs/cfc12/flasks/OldGC/',
            'N2O': f'{ftp_path}/n2o/flasks/OldGC/'}


class MSD_M3:
    """ MSD data from Montzka files """

    def __init__(self):
        self.instrument = 'msd'
        self.sites = ('alt', 'brw', 'cgo', 'hfm', 'kum', 'lef', 'mhd', 'mlo',
            'nwr', 'psa', 'smo', 'spo', 'sum', 'thd', 'ush')
        self.molpaths = {
            'F11': f'{ftp_path}/cfcs/cfc11/flasks/GCMS/CFC11b_GCMS_flask.txt',
            'F113': f'{ftp_path}/cfcs/cfc113/flasks/GCMS/CFC113_GCMS_flask.txt',
            'F12': f'{ftp_path}/cfcs/cfc12/flasks/GCMS/CFC12_GCMS_flask.txt',
            'h1211': f'{ftp_path}/halons/flasks/HAL1211_GCMS_flask.txt',
            'h2402': f'{ftp_path}/halons/flasks/Hal2402_GCMS_flask.txt',
            'HCFC141b': f'{ftp_path}/hcfcs/hcfc141b/HCFC141B_GCMS_flask.txt',
            'HCFC142b': f'{ftp_path}/hcfcs/hcfc142b/flasks/HCFC142B_GCMS_flask.txt',
            'HCFC22': f'{ftp_path}/hcfcs/hcfc22/flasks/HCFC22_GCMS_flask.txt',
            'HFC152a': f'{ftp_path}/hfcs/hf152a_GCMS_flask.txt',
            'HFC134a': f'{ftp_path}/hfcs/hfc134a_GCMS_flask.txt',
            'HFC365mfc': f'{ftp_path}/hfcs/HFC-365mfc_GCMS_flask.txt',
            'HFC227ea': f'{ftp_path}/hfcs/HFC-227ea_GCMS_flask.txt',
            'CH3Br': f'{ftp_path}/methylhalides/ch3br/flasks/CH3BR_GCMS_flask.txt',
            'CH3Cl': f'{ftp_path}/methylhalides/ch3cl/flasks/CH3Cl_GCMS_flask.txt',
            'C2Cl4': f'{ftp_path}/solvents/C2Cl4/flasks/pce_GCMS_flask.txt',
            'CH2Cl2': f'{ftp_path}/solvents/CH2Cl2/flasks/ch2cl2_GCMS_flask.txt',
            'MC': f'{ftp_path}/solvents/CH3CCl3/flasks/GCMS/CH3CCL3_GCMS_flask.txt',
            'OCS': f'{ftp_path}/carbonyl_sulfide/OCS__GCMS_flask.txt'
        }


class Common:
    """ Methods common to all FTP loaders """

    def __init__(self):
        super().__init__()
        # data directory used to store pickled version of pandas data panels.
        self.pklpath = '/hats/gc/cats_results/pkl_data'
        if not os.path.exists(self.pklpath):
            os.mkdir(self.pklpath)

    def ftppath(self, mol):
        """ Returns the base ftp path to CATS data determined by molecule """
        mol = self.mol_conversion(mol)
        if mol in self.molpaths:
            # self.molpaths is defined in each instrument class
            pt = self.molpaths[mol]
        else:
            print(f"Can't determine ftppath for {self.instrument}, molecule {mol}.")
            pt = None
        return pt

    def ftp_updatetime(self, mol):
        """ returns a time (floating point number) of the most recent updated file
            in the ftp path """
        path = self.ftppath(mol)
        if path is None:
            return 0
        files = glob.glob(path+'/monthly/*')
        if len(files) == 0:
            return 0
        else:
            return max([os.path.getmtime(f) for f in files])

    def mol_conversion(self, mol):
        """ converts a mol string to the correct upper and lower case. The dict
            good contains the correct cases. Returns all caps if not in dict.
        """
        good = {'CCL4': 'CCl4', 'CHCL3': 'CHCl3', 'CH3CL': 'CH3Cl', 'CH3CL': 'CH3Cl',
            'CH3BR': 'CH3Br', 'HFC142B': 'HFC142b', 'H1211': 'h1211', 'COS': 'OCS',
            'F134A': 'HFC134a', 'HFC134A': 'HFC134a', 'HFC365MFC': 'HFC365mfc', 'HFC227EA': 'HFC227ea',
            'F11B': 'F11'}
        if mol.upper() in good:
            return good[mol.upper()]
        return mol.upper()

    def fix_column_names(self, mol, site, cols):
        """ function to cleanup dataframe column names from CATS ftp files """
        cols = [x.replace(f'{mol.upper()}cats', '') for x in cols]
        cols = [x.replace(f'{mol.upper()}rits', '') for x in cols]
        cols = [x.replace(f'{mol.upper()}otto', '') for x in cols]
        cols = [x.replace(f'{site.upper()}', f'{site.lower()}_') for x in cols]
        cols = [x.replace('_msd', '_sd') for x in cols]
        cols = [x.replace('_m', '_mr') for x in cols]
        cols = [x.lower() for x in cols]
        return cols

    def gapfill(self, df, key='mr', smooth=True, forecast=False):
        """ Attempts to fit a seasonal ARIMAX model to a column of a dataframe.  If the
            fit is successful, estimate a 12 month forecast and use the fit and forecast
            to create a "gap filled" version of the data.
            Note: this method modifies the original dataframe df with new columns.
        """
        import statsmodels.api as sm

        # first and last good points (skips over nans)
        pt0 = df[key].first_valid_index()
        pt1 = df[key].last_valid_index()
        # find the column name of the 'sd' data.
        sdkey = [s for s in df.columns if 'sd' in s]

        """ seasonal ARIMAX model
            is set to only work on monthly data.  I could add a check to make sure
            the data is at the correct rate...
        """
        # force df.index to be inferred to prevent statsmodel warning (GSD 200226)
        df.index = pd.DatetimeIndex(df.index.values,
                freq=df.index.inferred_freq)
        mod = sm.tsa.statespace.SARIMAX(df[key][pt0:],
                order=(1, 1, 0), seasonal_order=(1, 1, 1, 12))
        try:
            results = mod.fit(disp=0)
        except ValueError:
            """ This error can occur when the dataset is too short  """
            print('SARIMAX failed to fit for {}'.format(self.site))
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
            df.loc[pt1:, 'gf'] = df.loc[pt1:, 'forecast']
            df.drop(['forecast'], axis=1, inplace=True)

        # interpolate any missing data that the "model" doesn't fill in.
        # inplace=True does not work
        df['gf'].update(df.loc[pt0:pt1, 'gf'].interpolate(method='time'))
        # missing gfsd are filled in with median of sd
        df['gfsd'] = df[sdkey].fillna(df[sdkey].median())
        df.loc[:pt0-relativedelta(months=1), 'gfsd'] = np.nan
        df.loc[pt1+relativedelta(months=1):, 'gfsd'] = np.nan
        # need to add forcast error for gfsd

        # rolling mean smooth if True
        if smooth:
            df['gf'].update(df['gf'].rolling(3, center=True).median())
            # replace first and last points that are lost due to smoothing.
            df.loc[pt0, 'gf'] = df.loc[pt0, key]
            df.loc[pt1, 'gf'] = df.loc[pt1, key]

        return df

    def loadall_multi(self, mol, reload=False, gapfill=True, smooth=True, forecast=False):
        """ Returns a pandas multi-index.  Also fits
            SARIMAX model and adds model, forecast, 'gf'(gap fill) columns to the panel
            ONLY Monthly data.
            Creates a pickle file of the panel and loads it if newer than ftp data.

            Options:
            Set reload to True to force a reload of FTP data (remakes pickle file)
            Set gapfill to False for no gap filling
            Set forecast to True to add the SARIMAX forecast to the end of the gap fill column

            Here is how to look at one site with multindex:
            df.loc['brw','2017']
        """
        mol = self.mol_conversion(mol)

        # load pickled version of multi if newer than ftp data.
        pklfile = f'{self.pklpath}/{self.instrument}_{mol}.pkl'
        if os.path.isfile(pklfile) and reload is False:
            p_date = os.path.getmtime(pklfile)
            f_date = self.ftp_updatetime(mol)
            if p_date > f_date:
                p = pd.read_pickle(pklfile)
                return p

        # load and make pandas data multi-index with all of the monthly median data
        dfs = []
        for site in self.sites:
            c = self.monthly(mol, site)
            c.columns = [x.replace(f'{site}_', '') for x in c.columns]
            if 'mr' in c.columns:
                c = self.gapfill(c, forecast=forecast, smooth=smooth) if gapfill else c
            c.rename_axis('date', inplace=True)
            c['site'] = site
            dfs.append(c)

        df = pd.concat(dfs, axis=0)
        df.reset_index(inplace=True)
        df.set_index(['site', 'date'], inplace=True)
        df.sort_index(inplace=True)
        df.to_pickle(pklfile)
        return df


class CATS_FTP(Common, CATS):
    """ Class for loading CATS data from the ftp server.
    """

    def __init__(self):
        super().__init__()

    def __dateParser_hourly(self, y, m, d, h, mn):
        return datetime(int(y), int(m), int(d), int(h), int(mn))

    def hourly(self, mol, site):
        """ Loads a CATS hourly data file.
            returns a dataframe with time as the index and conc, sd
        """
        mol = self.mol_conversion(mol)
        filename = f'hourly/{site.lower()}_{mol}_All.dat'
        if mol == 'h1211':
            filename = f'hourly/{site.lower()}_H1211_All.dat'
        if mol == 'CHCl3':
            filename = f'{site.lower()}_{mol}_All.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            na_values=['Nan'],  # pandas use 'nan', added 'Nan' to na_values
            parse_dates={'date': [0, 1, 2, 3, 4]},
            date_parser=self.__dateParser_hourly,
            index_col='date')
        df.columns = self.fix_column_names(mol, site, df.columns)
        return df

    def daily(self, mol, site):
        """ Loads a CATS daily data file.
        """
        mol = self.mol_conversion(mol)
        filename = f'daily/{site.lower()}_{mol}_Day.dat'
        if mol == 'h1211':
            filename = f'daily/{site.lower()}_H1211_Day.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1, 2]}, infer_datetime_format=True,
            index_col='date')
        df.columns = self.fix_column_names(mol, site, df.columns)
        return df

    def monthly(self, mol, site):
        """ Loads a CATS monthly median data file.
        """
        self.site = site    # this is needed for gapfill method
        mol = self.mol_conversion(mol)
        filename = f'monthly/{site.lower()}_{mol}_MM.dat'
        if mol == 'h1211':
            filename = f'monthly/{site.lower()}_H1211_MM.dat'
        elif mol == 'CHCl3':
            filename = f'{site.lower()}_{mol}_MM.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')
        if df.shape[1] == 3:
            df.columns = ['mr', 'sd', 'n']
        else:
            df.columns = ['mr', 'unc', 'sd', 'n']
        return df

    def globalmedian(self, mol):
        """ Loads a CATS global median data file.
        """
        mol = self.mol_conversion(mol)
        filename = f'global/insitu_global_{mol}.txt'
        if mol == 'h1211':
            filename = 'global/insitu_global_H1211.txt'

        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')
        df.columns = [x.replace('insitu_', '') for x in df.columns]
        df.columns = [x.lower() for x in df.columns]
        return df

    def display(self, mol, site, rate='monthly'):
        """ loads and displays CATS ftp data.
            monthly data by default, set rate to hourly or daily otherwise.
        """
        import matplotlib.pyplot as plt

        freq = getattr(CATS_FTP, rate, CATS_FTP.monthly)
        df = freq(self, mol, site)
        plt.plot(df.iloc[:, 0: 1], marker='o')        # plot first column which should be conc
        plt.ylabel('{} {}'.format(site.upper(), mol.upper()))
        plt.xlabel('date')
        plt.show()


class RITS_FTP(Common, RITS):
    """ Class for loading RITS data from the ftp server.
    """

    def __init__(self):
        super().__init__()
        self.rates = ('hourly', 'daily', 'monthly')

    def __dateParser_hourly(self, y, m, d, h, mn):
        return datetime(int(y), int(m), int(d), int(h), int(mn))

    def hourly(self, mol, site):
        """ Loads a RITS hourly data file.
            returns a dataframe with time as the index and conc, sd
        """
        mol = self.mol_conversion(mol)
        filename = f'hourly/{site.lower()}_{mol}_All.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            na_values=['Nan'],  # pandas use 'nan', added 'Nan' to na_values
            parse_dates={'date': [0, 1, 2, 3, 4]},
            date_parser=self.__dateParser_hourly,
            index_col='date')
        df.columns = self.fix_column_names(mol, site, df.columns)
        return df

    def daily(self, mol, site):
        """ Loads a RITS daily data file.
        """
        mol = self.mol_conversion(mol)
        filename = f'daily/{site.lower()}_{mol}_Day.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1, 2]}, infer_datetime_format=True,
            index_col='date')
        df.columns = self.fix_column_names(mol, site, df.columns)
        return df

    def monthly(self, mol, site):
        """ Loads a RITS monthly median data file.
        """
        self.site = site    # this is needed for gapfill method
        mol = self.mol_conversion(mol)
        filename = f'monthly/{site.lower()}_{mol}_MM.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')
        df.columns = self.fix_column_names(mol, site, df.columns)
        return df

    def globalmedian(self, mol):
        """ Loads a RITS global median data file.
        """
        mol = self.mol_conversion(mol)
        filename = f'global/insitu_global_{mol}.txt'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')
        df.columns = [x.replace(f'insitu_{mol.upper()}', '') for x in df.columns]
        df.columns = [x.lower() for x in df.columns]
        return df


class OTTO_FTP(Common, Otto):
    """ Class for loading OTTO data from the ftp server.
    """

    def __init__(self):
        super().__init__()
        self.rates = ('pairs', 'monthly')

    def pairs(self, mol, site):
        """ Loads a OTTO pair file.
        """
        mol = self.mol_conversion(mol)
        filename = f'pairs/{site.lower()}_{mol}_All.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1, 2]}, infer_datetime_format=True,
            index_col='date')
        df.columns = self.fix_column_names(mol, site, df.columns)
        return df

    def monthly(self, mol, site):
        """ Loads a OTTO monthly mean data file.
        """
        self.site = site    # this is needed for gapfill method
        mol = self.mol_conversion(mol)
        filename = f'monthly/{site.lower()}_{mol}_MM.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')
        df.columns = self.fix_column_names(mol, site, df.columns)
        return df


class OldGC_FTP(Common, OldGC):
    """ Load the original "Old" flask gc data.  Only monthly means are available. """

    def __init__(self):
        super().__init__()

    def monthly(self, mol, site, strip=False):
        """ Loads a Old Flask GC monthly mean data file.
        """
        self.site = site
        mol = mol.upper()
        filename = f'monthly/{site.upper()}_{mol}_MM.dat'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')
        lsite = site.lower()
        if strip:
            df.columns = ['mr', 'sd', 'n']
        else:
            df.columns = [f'{lsite}_mr', f'{lsite}_sd', f'{lsite}_n']
        return df


class CombinedData_FTP(Common):
    """ Load a HATS combined data file. """

    def __init__(self, mol='n2o'):
        super().__init__()
        self.mol = mol
        self.df = self.load_combined(mol)

    def ftppath(self, mol):
        """ Returns the base ftp path to Old Flask data determined by molecule """
        ftp = f'{ftp_path}'
        p = {'F11': '/cfcs/cfc11/combined/',
             'F12': '/cfcs/cfc12/combined/',
             'N2O': '/n2o/combined/',
             'SF6': '/sf6/combined/',
             'CCl4': '/solvents/CCl4/combined/'}
        if mol in p.keys():
            pt = ftp + p[mol]
        else:
            print(f"Can't determine ftppath for Combined Data file, molecule {mol}")
            pt = None
        return pt

    def load_combined(self, mol):
        mol = self.mol_conversion(mol)
        filename = f'HATS_global_{mol}.txt'
        try:
            fullpath = self.ftppath(mol)+filename
        except TypeError:
            return pd.DataFrame()
        df = pd.read_csv(fullpath, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')

        df.columns = [x.replace('HATS_', '') for x in df.columns]
        df.columns = [x.replace('GMD_', '') for x in df.columns]
        df.columns = [x.replace(f'_{mol}', '') for x in df.columns]

        return df


class MSD_FTP(Common, MSD_M3):

    def __init__(self):
        super().__init__()

    def pairs(self, mol):
        """ Load MSD flask pair means """
        mol = self.mol_conversion(mol)
        filename = self.molpaths[mol]
        msd = pd.read_csv(filename, sep='\\s+', header=1,
            names=['site', 'dec_date', 'yyymmdd', 'hhmmss', 'wind_dir', 'wind_spd', 'mr', 'sd'],
            parse_dates={'date': [2, 3]},
            index_col='date', na_values=['nd', '0.0'])
        msd.drop(['dec_date', 'wind_dir', 'wind_spd'], axis=1, inplace=True)
        msd.reset_index(inplace=True)
        msd.set_index(['site', 'date'], inplace=True)
        return msd

    def monthly(self, mol, gapfill=False):
        """ Monthly means calculated from flask pair means """
        df = self.pairs(mol)
        # don't know of an easier method for resampling a pandas multiindex
        df = df.reset_index('site').groupby('site').resample('MS').mean().reset_index().set_index(['site', 'date'])

        if gapfill:
            dfs = []
            for site in set(df.reset_index()['site']):  # background sites
                c = df.loc[site]
                if 'mr' in c.columns:
                    c = self.gapfill(c, forecast=True, smooth=True)
                c.rename_axis('date', inplace=True)
                c['site'] = site
                dfs.append(c)

            df = pd.concat(dfs, axis=0)
            df.reset_index(inplace=True)
            df.set_index(['site', 'date'], inplace=True)
            df.sort_index(inplace=True)

        return df


class HATS():

    def monthly(self, mol):
        ftp = CATS_FTP()
        cats = ftp.loadall(mol, 'monthly')
        cats.columns = [x.replace(mol.upper()+'cats', '') for x in cats.columns]
        cats['inst'] = 'CATS'
        ftp = OldGC_FTP()
        old = ftp.loadall(mol)
        old.columns = [x.replace(mol.upper()+'oldGC', '') for x in old.columns]
        old['inst'] = 'oldGC'
        all = pd.concat([old, cats])
        return all


if __name__ == '__main__':

    cats = CATS_FTP()
    otto = OTTO_FTP()
    old = OldGC_FTP()
    comb = CombinedData_FTP()
    # df = cats.globalmedian('ccl4')
    # df = otto.pairs('f11', 'brw')
    # df = old.loadall('f11')
    df = comb.load_combined('n2o')
    print(df.head(10))
    # print(df.describe())


"""
# method to load from URL instead of /aftp path
dataset1 = 'ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/CATS/monthly/brw_F11_MM.dat'
dataset2 = 'ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/flasks/Otto/monthly/brw_F11_MM.dat'
dataset3 = 'ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/RITS/monthly/brw_F11_MM.dat'
dataset4 = 'ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/flasks/OldGC/monthly/BRW_F11_MM.dat'

def loaddata(dataset):
    return pd.read_csv(dataset, delim_whitespace=True, comment='#',
        parse_dates = {'date':[0,1]}, infer_datetime_format=True, index_col = 'date')
"""
