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

    TODO: add 'oldgc', 'otto', and the combinded data sets to the loader. """

import pandas as pd
from datetime import datetime
import multiprocessing as mp

import halocarbon_urls
from gapfill import Gap_Methods


class HATS_Loader(halocarbon_urls.HATS_MSD_URLs):

    def __init__(self):
        super().__init__()
        self.gases = list(self.urls.keys())

    def gas_conversion(self, gas):
        """ converts a gas string to the correct upper and lower case. The dict
            good contains the correct cases. Returns all caps if not in dict. """

        good = {'CCL4': 'CCl4', 'CHCL3': 'CHCl3', 'CH3CL': 'CH3Cl', 'CH3CL': 'CH3Cl',
            'CH3BR': 'CH3Br', 'HFC142B': 'HFC142b', 'H1211': 'h1211', 'COS': 'OCS',
            'F134A': 'HFC134a', 'HFC134A': 'HFC134a', 'HFC365MFC': 'HFC365mfc',
            'HFC227EA': 'HFC227ea', 'F11B': 'F11',
            'H1211': 'h1211', 'H1301': 'h1301', 'H2402': 'h2402'}

        if gas.upper() in good:
            return good[gas.upper()]
        return gas.upper()

    def loader(self, gas, **kwargs):
        """ Main loader method. """
        gas = self.gas_conversion(gas)

        # keywords used in loader with default values
        program = kwargs.get('program', 'MSD')
        freq = kwargs.get('freq', 'monthly')
        gapfill = kwargs.get('gapfill', False)
        verbose = kwargs.get('verbose', True)

        if program.upper() in ['M3', 'PR1', 'MSD']:
            hats = MSDs(verbose=verbose)
            if freq == 'pairs':
                return hats.pairs(gas)
            else:
                return hats.monthly(gas, gapfill=gapfill)
        elif program.upper() in ['CATS', 'RITS', 'INSITU']:
            hats = insitu(verbose=verbose, prog=program)
            return hats.insitu_loader(gas, freq=freq)


class MSDs(halocarbon_urls.HATS_MSD_URLs):

    def __init__(self, verbose=True):
        super().__init__()
        self.verbose = verbose

    def pairs(self, gas):
        """ Load MSD flask pair means """
        try:
            filename = self.urls[gas]
        except KeyError:
            print(f'Unknown gas name: {gas}')
            print(f'Choose from: {sorted(list(self.urls.keys()))}')
            quit()

        # determine file type "M3" or "PR1"
        type = 'PR1' if filename.find('PR1') > 0 else 'GCMS'

        if self.verbose:
            print(f'Loading data for {gas}')
            print(f'File URL: {filename}')
            print('Please consult the header in the file listed above for PI and contact information.')

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
        msd.set_index(['site', 'date'], inplace=True)
        return msd

    def monthly(self, gas, gapfill=False):
        """ Monthly means calculated from flask pair means """
        df = self.pairs(gas)

        # A monthly mean of these columns doesn't make sense. Dropping them.
        df = df.drop(['dec_date', 'wind_dir', 'wind_spd', 'flag', 'inst'], axis=1, errors='ignore')

        # resample pandas multiindex by site
        df = df.reset_index('site').groupby('site').resample('MS').mean().reset_index().set_index(['site', 'date'])

        if gapfill:
            from time import time
            t0 = time()
            sites = set(df.reset_index()['site'])
            with mp.Pool() as p:
                res = p.starmap(self.gapfiller, [(df, s) for s in sites])

            df = pd.concat(res)
            df.reset_index(inplace=True)
            df.set_index(['site', 'date'], inplace=True)
            df.sort_index(inplace=True)
            print(f'gapfiller took {time()-t0:.1f} seconds')

        return df

    def gapfiller(self, df, site):
        gap = Gap_Methods()
        sub_df = df.loc[site]
        if 'mf' in sub_df.columns:
            sub_df = gap.robust_seasonal(sub_df, forecast=True)
        sub_df.rename_axis('date', inplace=True)
        sub_df['site'] = site
        return sub_df


class insitu(halocarbon_urls.insitu_URLs):
    """ Class for loading CATS data from the GML FTP server.
    """

    def __init__(self, verbose=True, prog='CATS'):
        super().__init__(prog)
        self.verbose = verbose
        self.prog = prog.upper()
        self.mp_processes = 3

    def insitu_csv_reader(self, gas, freq, site):
        urls = self.urls(site, freq=freq)
        url = urls[gas]

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
        return df

    def __dateParser_hourly(self, y, m, d, h, mn):
        return datetime(int(y), int(m), int(d), int(h), int(mn))

    def insitu_loader(self, gas, freq='monthly'):
        """ Load CATS or RITS data for all sites. This method uses
            multiprocessing to simultaneously load files from the FTP site. """

        if gas not in self.gases:
            print(f'{self.prog} does not measure {gas}')
            return

        if self.verbose:
            print(f'Loading data for {gas}')

        # processes can't be too large or ftp server complains
        with mp.Pool(processes=self.mp_processes) as p:
            # step through each insitu site.
            res = p.starmap(self.insitu_csv_reader, [(gas, freq, s) for s in self.sites])

        # create a single dataframe
        df = pd.concat(res)
        df.reset_index(inplace=True)
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
