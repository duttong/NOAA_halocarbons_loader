#! /usr/bin/env python

""" Methods for loading NOAA/GML halocarbon data from the NOAA/GML FTP site
    located at: ftp://ftp.cmdl.noaa.gov/hats

    There are several measurement programs for halocarbon data. The loader
    method in the class HATS_Loader will return monthly mean flask data
    measured on the M3 mass spectrometer instrument. To select data from a
    different measurement program use the 'program' key word. Valid flask measurement
    programs include 'M3', 'otto', 'oldgc'. Use 'CATS' or 'RITS' for in situ
    measurements.

    The 'freq' key word is short for measurement frequence. All programs return
    monthly means or medians. 'freq' can be set to 'daily' or 'hourly' for the
    in situ measurement programs.
"""

import pandas as pd
from datetime import datetime
import multiprocessing as mp
from time import time, sleep

import halocarbon_urls
from gapfill import Gap_Methods


class HATS_Loader(halocarbon_urls.HATS_MSD_URLs):

    def __init__(self):
        super().__init__()
        # list of all gases available on FTP site
        self.gases = list(self.urls.keys())     # MSD gases
        self.gases.append('N2O')    # add N2O and CCl4 (non MSD gases)
        self.gases.append('CCl4')
        self.gases = sorted(self.gases)
        self.gasloaded = ''
        # pandas data frame with GML site info
        self.gml_sites = self.gml_sites()
        # background air measurement sites
        self.bk_sites = ('alt', 'sum', 'brw', 'cgo', 'kum', 'mhd', 'mlo', 'nwr', 'thd', 'smo', 'ush', 'psa', 'spo')
        self.programs_msd = ('m3', 'pr1', 'msd')
        self.programs_insitu = ('rits', 'cats', 'insitu')
        self.programs_flaskECD = ('oldgc', 'otto')
        self.programs_combined = ('combined', 'combine', 'combo')

    def gml_sites(self):
        """ Site info from the GML DB """
        try:
            df = pd.read_csv('sites.csv')
        except FileNotFoundError:
            # path if cloned from github
            df = pd.read_csv('NOAA_halocarbons_loader/sites.csv')
        return df

    def loader(self, gas, program='msd', freq='monthly', gapfill=False, addlocation=True, verbose=True):
        """ Main loader method. """
        gas = self.gas_conversion(gas)
        self.gasloaded = gas

        program = program.lower()
        freq = freq.lower()

        if (gas == 'N2O' or gas == 'CCl4') & (program == 'msd'):
            print(f'The MSD program does not measure {gas} the returned cats_results are from the Combined Data Set.')
            program = 'combined'

        if program in self.programs_msd:
            hats = MSDs(verbose=verbose)
            if freq == 'pairs':
                df = hats.pairs(gas)
            else:
                df = hats.monthly(gas, gapfill=gapfill)

        elif program in self.programs_insitu:
            hats = insitu(verbose=verbose, prog=program)
            df = hats.insitu_loader(gas, freq=freq)

        elif program in self.programs_flaskECD:
            hats = Flasks(verbose=verbose, prog=program)
            df = hats.flask_loader(gas, freq=freq)

        elif program in self.programs_combined:
            hats = Combined(verbose=verbose)
            df = hats.combo_loader(gas)

        else:
            print(f'Unknown measurement program: {program}')
            return

        # the loader did not return any data
        if df.shape[0] == 0:
            return

        if gapfill and (freq == 'monthly'):
            if program not in self.programs_combined:    # combined data already gapfilled
                t0 = time()
                sites = set(df.reset_index()['site'])
                method = 'linear' if program == 'oldgc' else 'seasonal'
                print(f'{method} gapfill started')
                with mp.Pool() as p:
                    res = p.starmap(self.gapfiller, [(df, s, method) for s in sites])

                df = pd.concat(res)
                df.reset_index(inplace=True)
                df.set_index(['site', 'date'], inplace=True)
                df.sort_index(inplace=True)
                print(f'gapfiller took {time()-t0:.1f} seconds')

        # insert lat, lon, elev into dataframe
        if program not in self.programs_combined and addlocation:
            df = self.add_location(df)

        # add meta data to dataframe (this is exerimental as of 2021)
        df.attrs['gas'] = gas
        df.attrs['program'] = program

        return df

    def add_location(self, df_org):
        """ Add lat, lon, and elev based on data in the self.gml_sites dataframe """
        df = df_org.copy().reset_index()
        for site in df.site.unique():
            lat = self.gml_sites.loc[self.gml_sites['site'] == site.upper()].lat.values[0]
            lon = self.gml_sites.loc[self.gml_sites['site'] == site.upper()].lon.values[0]
            elev = self.gml_sites.loc[self.gml_sites['site'] == site.upper()].elev.values[0]
            df.loc[df.site == site, 'lat'] = lat
            df.loc[df.site == site, 'lon'] = lon
            df.loc[df.site == site, 'elev'] = elev

        df = df.set_index(['site', 'date'])
        return df

    def gas_conversion(self, gas):
        """ Converts a gas string to the correct upper and lower case. The dict
            subs are substitutions or commonly used aliases. """

        # N2O and CCl4 are not in the self.gases list
        # the keys should be in all uppercase
        subs = {'F11B': 'F11', 'COS': 'OCS',
                'MC': 'CH3CCl3', 'CT': 'CCl4',
                '1211': 'h1211', '1301': 'h1301', '2402': 'h2402',
                'CFC11': 'F11', 'CFC12': 'F12', 'CFC113': 'F113',
                '11': 'F11', '113': 'F113', '114': 'F114', '115': 'F115',
                '12': 'F12', '13': 'F13',
                '123': 'HCFC123', '124': 'HCFC124', '133A': 'HCFC133a', '133': 'HCFC133a',
                '141B': 'HCFC141b', '141': 'HCFC141b', '142B': 'HCFC142b', '142': 'HCFC142b',
                '22': 'HCFC22', '125': 'HFC125', '134A': 'HFC134a', '134': 'HFC134a',
                '143A': 'HFC143a', '143': 'HFC143a', '152A': 'HFC152a', '152': 'HFC152a'}

        # first compare to substitutions
        if gas.upper() in subs:
            proper = subs[gas.upper()]
        # now compare to the gases in the urls key
        elif gas.casefold() in (g.casefold() for g in self.gases):
            proper = self._casecompare(gas)
        else:
            print(f'NOAA/GML does not measure {gas}')
            proper = gas
        return proper

    def _casecompare(self, gas):
        """ Returns the correct case as it appears in self.gases """
        for g in self.gases:
            if gas.casefold() == g.casefold():
                return g

    def mf_units(self, gas):
        units = '(ppb)' if gas == 'N2O' else '(ppt)'
        return units

    def bk_sites_figure(self, df):
        """ Plot the background air measurement sites. """
        import matplotlib.pyplot as plt
        dfsites = df.reset_index()['site'].unique()
        for site in dfsites:
            if site in self.bk_sites:
                df['mf'][site].plot(label=site)

        plt.legend()
        plt.ylabel(f'{self.gasloaded} mole fraction {self.mf_units(self.gasloaded)}')
        plt.title('Background Stations')
        plt.show()

    def gapfiller(self, df, site, method='seasonal'):
        gap = Gap_Methods()
        sub_df = df.loc[site]
        if 'mf' in sub_df.columns:
            # print(f'{method} gap fill at {site}')
            if method == 'seasonal':
                sub_df = gap.robust_seasonal(sub_df, forecast=True)
            elif method == 'linear':
                sub_df = gap.linear(sub_df)
            else:
                pass
            sub_df['mf'] = sub_df['gf']
            sub_df['sd'] = sub_df['gfsd']
            sub_df.drop(['gf', 'gfsd'], axis=1, inplace=True)
        sub_df.rename_axis('date', inplace=True)
        sub_df['site'] = site
        return sub_df

    def multi_instrument_dataframe(self, list_dfs):
        """ Create a synced dataframe from a list of measurement program
            dataframes, list_dfs """

        dfs = []

        # iterate through program dataframes for mf and sd
        for df in list_dfs:
            if df is None:
                print('Blank dataframe in list. Skipping.')
                continue
            if df.shape[0] == 0:
                print('Blank dataframe in list. Skipping.')
                continue
            df = df.reset_index()
            df = df[['date', 'site', 'mf', 'sd', 'lat', 'lon', 'elev']]
            df['prog'] = df.attrs['program']
            dfs.append(df)

        # combine into one dataframe
        df = pd.concat(dfs)
        df = df.set_index('date').sort_index()

        # use attrs for meta data. In this case the gas name.
        df.attrs['gas'] = list_dfs[0].attrs['gas']

        return df
    

class MSDs(halocarbon_urls.HATS_MSD_URLs):
    """ More info about the flask program can be found here:
        https://www.esrl.noaa.gov/gmd/hats/flask/flasks.html """

    def __init__(self, verbose=True):
        super().__init__()
        self.verbose = verbose

    def pairs(self, gas):
        """ Load MSD flask pair means """
        try:
            filename = self.urls[gas]
        except KeyError:
            print(f'Choose from: {sorted(list(self.urls.keys()))}')
            return pd.DataFrame()

        if self.verbose:
            print(f'Loading data for {gas}')
            print(f'File URL: {filename}')
            print('Please consult the header in the file listed above for PI and contact information.')

        # determine file type "M3" or "PR1"
        type = 'PR1' if filename.find('PR1') > 0 else 'GCMS'

        if type == 'GCMS':
            msd = pd.read_csv(filename, sep='\\s+', header=1,
                names=['site', 'dec_date', 'yyymmdd', 'hhmmss', 'wind_dir', 'wind_spd', 'mf', 'sd'],
                parse_dates={'date': [2, 3]},
                index_col='date', na_values=['nd', '0.0'])
            msd['inst'] = 'M3'

        else:  # PR1 file type
            msd = pd.read_csv(filename, sep='\\s+', header=1, comment='#',
                names=['site', 'dec_date', 'yyymmdd', 'hhmm', 'wind_dir', 'wind_spd', 'mf', 'sd', 'flag', 'inst'],
                parse_dates={'date': [2, 3]},
                index_col='date', na_values=['nd', '0.0'])
            msd['site'] = msd['site'].str.lower()

        msd.reset_index(inplace=True)
        self.sites = msd['site'].unique()
        msd.set_index(['site', 'date'], inplace=True)
        return msd

    def monthly(self, gas, gapfill=False):
        """ Monthly means calculated from flask pair means """
        df = self.pairs(gas)

        # df is blank because MSD program doesn't measure the gas selected.
        if df.shape[0] == 0:
            return df

        # A monthly mean of these columns doesn't make sense. Dropping them.
        df = df.drop(['dec_date', 'wind_dir', 'wind_spd', 'flag', 'inst'], axis=1, errors='ignore')

        # resample pandas multiindex by site
        df = df.reset_index('site').groupby('site').resample('MS').mean().reset_index().set_index(['site', 'date'])

        return df


class insitu(halocarbon_urls.insitu_URLs):
    """ Class for loading CATS data from the GML FTP server.
    """

    def __init__(self, verbose=True, prog='CATS'):
        super().__init__(prog)
        self.verbose = verbose
        self.mp_processes = 6

    def insitu_csv_reader(self, gas, freq, site):
        try:
            urls = self.urls(site, freq=freq)
            url = urls[gas]
        except KeyError:
            print(f'The insitu program does not report data for: {gas}')
            print(f'Choose from: {self.gases}')
            return pd.DataFrame()

        if self.verbose:
            print(f'File URL: {url}')

        if freq == 'monthly':
            df = pd.read_csv(url, delim_whitespace=True, comment='#',
                parse_dates={'date': [0, 1]}, infer_datetime_format=True,
                index_col='date')

            # rename columns
            if df.shape[1] == 3:
                df.columns = ['mf', 'sd', 'n']
            else:
                df.columns = ['mf', 'unc', 'sd', 'n']

        elif freq == 'daily':
            df = pd.read_csv(url, delim_whitespace=True, comment='#',
                parse_dates={'date': [0, 1, 2]}, infer_datetime_format=True,
                index_col='date')
            df.columns = ['mf', 'unc', 'n']      # rename columns

        elif freq == 'hourly':
            df = pd.read_csv(url, delim_whitespace=True, comment='#',
                na_values=['Nan'],  # pandas use 'nan', added 'Nan' to na_values
                parse_dates={'date': [0, 1, 2, 3, 4]},
                date_parser=self.__dateParser_hourly,
                index_col='date')
            df.columns = ['mf', 'unc']

        df['site'] = site       # add site column

        # sleep(1)    # slow down, don't hammer the FTP site with requests

        return df

    def __dateParser_hourly(self, y, m, d, h, mn):
        return datetime(int(y), int(m), int(d), int(h), int(mn))

    def insitu_loader(self, gas, freq='monthly', gapfill=False):
        """ Load CATS or RITS data for all sites. This method uses
            multiprocessing to simultaneously load files from the FTP site. """

        if gas not in self.gases:
            print(f'{self.prog} does not measure {gas}')
            print(f'Choose from: {self.gases}')
            return pd.DataFrame()

        if self.verbose:
            print(f'Loading data for {gas}')

        # processes can't be too large or ftp server complains
        with mp.Pool(processes=self.mp_processes) as p:
            # step through each insitu site.
            res = p.starmap(self.insitu_csv_reader, [(gas, freq, s) for s in self.sites])

        # create a single dataframe
        df = pd.concat(res)
        df.reset_index(inplace=True)
        self.sites = df['site'].unique()
        df.set_index(['site', 'date'], inplace=True)
        df.sort_index(inplace=True)

        if self.verbose:
            print('Please consult the header in the files listed above for PI and contact information.')

        return df

    def globalmedian(self, gas):
        """ Loads a CATS global median data file.
            NOT FINISHED
        """
        df = pd.read_csv(gas, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')
        df.columns = [x.replace('insitu_', '') for x in df.columns]
        df.columns = [x.lower() for x in df.columns]
        return df


class Flasks(halocarbon_urls.Flask_GCECD_URLs):
    """ Class for loading Flask data from the GML FTP server.
        More info about the flask program can be found here:
        https://www.esrl.noaa.gov/gmd/hats/flask/flasks.html """

    def __init__(self, verbose=True, prog='Otto'):
        super().__init__(prog)
        self.verbose = verbose
        self.mp_processes = 6       # number of processors to use for FTP download

    def flask_csv_reader(self, gas, freq, site):
        urls = self.urls(site, freq=freq)
        url = urls[gas]

        if self.verbose:
            print(f'File URL: {url}')

        if freq == 'monthly':
            df = pd.read_csv(url, delim_whitespace=True, comment='#',
                parse_dates={'date': [0, 1]}, infer_datetime_format=True,
                index_col='date')
            df.columns = ['mf', 'sd', 'n']

        elif freq == 'hourly':
            df = pd.read_csv(url, delim_whitespace=True, comment='#',
                na_values=['Nan'],  # pandas use 'nan', added 'Nan' to na_values
                parse_dates={'date': [0, 1, 2, 3, 4]},
                date_parser=self.__dateParser_hourly,
                index_col='date')
            df.columns = ['mf', 'unc']

        df['site'] = site       # add site column

        # sleep(1)    # slow down, don't hammer the FTP site with requests

        return df

    def flask_loader(self, gas, freq='monthly'):
        """ Load Otto or OldGC data for all sites. This method uses
            multiprocessing to simultaneously load files from the FTP site. """

        if gas not in self.gases:
            print(f'{self.prog} does not measure {gas}')
            print(f'Choose from: {self.gases}')
            return pd.DataFrame()

        if self.verbose:
            print(f'Loading data for {gas}')

        # processes can't be too large or ftp server complains
        with mp.Pool(processes=self.mp_processes) as p:
            # step through each insitu site.
            res = p.starmap(self.flask_csv_reader, [(gas, freq, s) for s in self.sites])

        # create a single dataframe
        df = pd.concat(res)
        df.reset_index(inplace=True)
        self.sites = df['site'].unique()
        df.set_index(['site', 'date'], inplace=True)
        df.sort_index(inplace=True)

        if self.verbose:
            print('Please consult the header in the files listed above for PI and contact information.')

        return df


class Combined(halocarbon_urls.Combined_Data_URLs):

    def __init__(self, verbose=True):
        super().__init__()
        self.verbose = verbose

    def combo_loader(self, gas):
        filename = self.urls[gas]

        if self.verbose:
            print(f'Loading data for {gas}')
            print(f'File URL: {filename}')
            print('Please consult the header in the file listed above for PI and contact information.')

        df = pd.read_csv(filename, delim_whitespace=True, comment='#',
            parse_dates={'date': [0, 1]}, infer_datetime_format=True,
            index_col='date')

        # shorten column names
        df.columns = [x.replace('HATS_', '') for x in df.columns]
        df.columns = [x.replace('GMD_', '') for x in df.columns]
        df.columns = [x.replace(f'_{gas}', '') for x in df.columns]
        df.columns = [x.replace(f'{gas}_', '') for x in df.columns]

        # make the Programs column a formatted string field
        df['Programs'] = df['Programs'].astype(str).apply('{:0>6}'.format)
        self.sites = ['alt', 'sum', 'brw', 'cgo', 'kum', 'mhd', 'mlo', 'nwr', 'thd', 'smo', 'ush', 'psa', 'spo']

        return df
