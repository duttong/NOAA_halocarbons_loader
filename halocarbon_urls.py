#! /usr/bin/env python

# baseftp = 'ftp://ftp.cmdl.noaa.gov/hats'
basehttp = 'https://www.esrl.noaa.gov/gmd/aftp/data/hats'


class HATS_MSD_URLs:

    def __init__(self):
        self.urls = self.msd_urls()

    def msd_urls(self):
        """ urls for GML's MSD flask measurements current as of 20210112
            Note, these are steel and glass flasks from the halocarbon network and
            does not include PFPs. 
            
            Updated urls to include the 2010 sting in the file name. 20231130 """
        u = {}

        # CFCs
        u['F11'] = f'{basehttp}/cfcs/cfc11/flasks/GCMS/CFC11b_GCMS_flask_2010.txt'
        u['F113'] = f'{basehttp}/cfcs/cfc113/flasks/GCMS/CFC113_GCMS_flask.txt'
        u['F12'] = f'{basehttp}/cfcs/cfc12/flasks/GCMS/CFC12_GCMS_flask_2010.txt'

        # halons
        u['h1211'] = f'{basehttp}/halons/flasks/HAL1211_GCMS_flask.txt'
        u['h2402'] = f'{basehttp}/halons/flasks/Hal2402_GCMS_flask.txt'
        u['h1301'] = f'{basehttp}/halons/flasks/H-1301_M2_PR1_MS_flask.txt'

        # HCFCs
        u['HCFC141b'] = f'{basehttp}/hcfcs/hcfc141b/HCFC141B_GCMS_flask.txt'
        u['HCFC142b'] = f'{basehttp}/hcfcs/hcfc142b/flasks/HCFC142B_GCMS_flask.txt'
        u['HCFC22'] = f'{basehttp}/hcfcs/hcfc22/flasks/HCFC22_GCMS_flask.txt'

        # HFCs
        u['HFC152a'] = f'{basehttp}/hfcs/hf152a_GCMS_flask.txt'
        u['HFC134a'] = f'{basehttp}/hfcs/hfc134a_GCMS_flask.txt'
        u['HFC143a'] = f'{basehttp}/hfcs/HFC-143a_M2_PR1_MS_flask.txt'
        u['HFC365mfc'] = f'{basehttp}/hfcs/HFC-365mfc_GCMS_flask.txt'
        u['HFC32'] = f'{basehttp}/hfcs/HFC-32_M2_PR1_MS_flask.txt'
        u['HFC227ea'] = f'{basehttp}/hfcs/HFC-227ea_GCMS_flask.txt'
        u['HFC125'] = f'{basehttp}/hfcs/HFC-125_M2_PR1_MS_flask.txt'

        # Methylhalides
        u['CH3Br'] = f'{basehttp}/methylhalides/ch3br/flasks/CH3BR_GCMS_flask.txt'
        u['CH3Cl'] = f'{basehttp}/methylhalides/ch3cl/flasks/CH3Cl_GCMS_flask.txt'

        # Solvents
        u['C2Cl4'] = f'{basehttp}/solvents/C2Cl4/flasks/pce_GCMS_flask.txt'
        u['CH2Cl2'] = f'{basehttp}/solvents/CH2Cl2/flasks/ch2cl2_GCMS_flask.txt'
        u['CH3CCl3'] = f'{basehttp}/solvents/CH3CCl3/flasks/GCMS/CH3CCL3_GCMS_flask.txt'

        # Carbonyl Sulfide (COS or OCS)
        u['OCS'] = f'{basehttp}/carbonyl_sulfide/OCS__GCMS_flask.txt'

        # PERSEUS specific gases
        u['C3H8'] = f'{basehttp}/PERSEUS/C3H8_PR1_MS_flask.txt'
        u['C2H6'] = f'{basehttp}/PERSEUS/C2H6_PR1_MS_flask.txt'
        u['CF4'] = f'{basehttp}/PERSEUS/CF4_PR1_MS_flask.txt'
        u['NF3'] = f'{basehttp}/PERSEUS/NF3_PR1_MS_flask.txt'
        u['PFC116'] = f'{basehttp}/PERSEUS/PFC-116_PR1_MS_flask.txt'
        u['SO2F2'] = f'{basehttp}/PERSEUS/SO2F2_PR1_MS_flask.txt'
        u['HFC236fa'] = f'{basehttp}/PERSEUS/HFC-236fa_PR1_MS_flask.txt'
        #u['C2Cl4'] = f'{basehttp}/PERSEUS/C2Cl4_PR1_MS_flask.txt'
        u['C2H2'] = f'{basehttp}/PERSEUS/C2H2_PR1_MS_flask.txt'
        u['F114'] = f'{basehttp}/PERSEUS/CFC-114_PR1_MS_flask.txt'
        u['F115'] = f'{basehttp}/PERSEUS/CFC-115_PR1_MS_flask.txt'
        u['F13'] = f'{basehttp}/PERSEUS/CFC-13_PR1_MS_flask.txt'
        u['HCFC123'] = f'{basehttp}/PERSEUS/HCFC-123_PR1_MS_flask.txt'
        u['HCFC124'] = f'{basehttp}/PERSEUS/HCFC-124_PR1_MS_flask.txt'
        u['HCFC133a'] = f'{basehttp}/PERSEUS/HCFC-133a_PR1_MS_flask.txt'
        #u['HFC125'] = f'{basehttp}/PERSEUS/HFC-125_PR1_MS_flask.txt'
        # use the M2 + PR1 file for HFC143a
        # u['HFC143a'] = f'{basehttp}/PERSEUS/HFC-143a_PR1_MS_flask.txt'
        # removed HFC23
        # u['HFC23'] = f'{basehttp}/PERSEUS/HFC-23_PR1_MS_flask.txt'
        # u['HFC32'] = f'{basehttp}/PERSEUS/HFC-32_PR1_MS_flask.txt'
        u['HFO1234yf'] = f'{basehttp}/PERSEUS/HFO-1234yf_PR1_MS_flask.txt'
        u['HFO1234ze'] = f'{basehttp}/PERSEUS/HFO-1234ze_PR1_MS_flask.txt'
        u['PFC218'] = f'{basehttp}/PERSEUS/PFC-218_PR1_MS_flask.txt'
        u['SF6'] = f'{basehttp}/PERSEUS/SF6_PR1_MS_flask.txt'
        u['i-butane'] = f'{basehttp}/PERSEUS/i-butane_PR1_MS_flask.txt'
        u['i-pentane'] = f'{basehttp}/PERSEUS/i-pentane_PR1_MS_flask.txt'
        u['n-butane'] = f'{basehttp}/PERSEUS/n-butane_PR1_MS_flask.txt'
        u['n-hexane'] = f'{basehttp}/PERSEUS/n-hexane_PR1_MS_flask.txt'
        u['n-pentane'] = f'{basehttp}/PERSEUS/n-pentane_PR1_MS_flask.txt'

        return u

    def which_MSD(self, url):
        msd = 'PR1' if url.find('PR1') > 0 else 'M3'
        return msd


class insitu_URLs:
    """ There have been two in situ halocarbon measurement programs in NOAA/GML
        The RITS program: https://www.esrl.noaa.gov/gmd/hats/insitu/insitu.html
        followd by the CATS program: https://www.esrl.noaa.gov/gmd/hats/insitu/cats/
        Both programs made about hourly measurements at 5 stations. CATS also made
        measurements at Summit, Greenland (sum) """

    def __init__(self, prog='CATS'):
        self.prog = prog.upper()

        self.sites = ['brw', 'nwr', 'mlo', 'smo', 'spo']
        if self.prog == 'CATS':
            self.sites.append('sum')    # additional site for CATS

        self.gases = list(self.urls('mlo').keys())

    def urls(self, site, freq='monthly'):
        """ URLs for the Chromatograph for Atmospheric Species (CATS) program as of 20210201 """
        u = {}
        suffix = {'hourly': 'All', 'daily': 'Day', 'monthly': 'MM'}

        # gases common to both insitu programs
        u['F11'] = f'{basehttp}/cfcs/cfc11/insituGCs/{self.prog}/{freq}/{site}_F11_{suffix[freq]}.dat'
        u['F12'] = f'{basehttp}/cfcs/cfc12/insituGCs/{self.prog}/{freq}/{site}_F12_{suffix[freq]}.dat'
        u['h1211'] = f'{basehttp}/halons/insituGCs/{self.prog}/{freq}/{site}_H1211_{suffix[freq]}.dat'
        u['N2O'] = f'{basehttp}/n2o/insituGCs/{self.prog}/{freq}/{site}_N2O_{suffix[freq]}.dat'
        u['CCl4'] = f'{basehttp}/solvents/CCl4/insituGCs/{self.prog}/{freq}/{site}_CCl4_{suffix[freq]}.dat'
        u['CH3CCl3'] = f'{basehttp}/solvents/CH3CCl3/insituGCs/{self.prog}/{freq}/{site}_MC_{suffix[freq]}.dat'

        # CATS additional gases
        if self.prog == 'CATS':
            u['F113'] = f'{basehttp}/cfcs/cfc113/insituGCs/{self.prog}/{freq}/{site}_F113_{suffix[freq]}.dat'
            u['SF6'] = f'{basehttp}/sf6/insituGCs/{self.prog}/{freq}/{site}_SF6_{suffix[freq]}.dat'

        return u


class Combined_Data_URLs:

    def __init__(self):
        self.urls = self.combo_urls()
        self.gases = self.urls.keys()

    def combo_urls(self):
        u = {}
        u['F11'] = f'{basehttp}/cfcs/cfc11/combined/HATS_global_F11.txt'
        u['F12'] = f'{basehttp}/cfcs/cfc12/combined/HATS_global_F12.txt'
        u['F113'] = f'{basehttp}/cfcs/cfc113/combined/HATS_global_F113.txt'
        u['CCl4'] = f'{basehttp}/solvents/CCl4/combined/HATS_global_CCl4.txt'
        u['N2O'] = f'{basehttp}/n2o/combined/GML_global_N2O.txt'
        u['SF6'] = f'{basehttp}/sf6/combined/GML_global_SF6.txt'
        return u

class Flask_GCECD_URLs:
    """Refactored URL builder for Otto, fECD, and OldGC programs"""
    BASE_URL = basehttp  # ensure basehttp is defined in the module

    # Available sites per program
    PROGRAM_SITES = {
        'Otto': ('alt', 'sum', 'brw', 'cgo', 'kum', 'mhd', 'mlo', 'nwr', 'thd', 'smo', 'ush', 'psa', 'spo'),
        'fECD': ('alt', 'sum', 'brw', 'cgo', 'kum', 'mhd', 'mlo', 'nwr', 'thd', 'rpb', 'smo', 'ush', 'psa', 'spo'),
        'OldGC': ('alt', 'brw', 'cgo', 'nwr', 'mlo', 'smo', 'spo'),
    }

    # Gas to path mapping and optional override codes
    GAS_PATHS = {
        'F11': ('cfcs/cfc11', None),
        'F12': ('cfcs/cfc12', None),
        'F113': ('cfcs/cfc113', None),
        'N2O': ('n2o', None),
        'SF6': ('sf6', None),
        'CCl4': ('solvents/CCl4', None),
        'CH3CCl3': ('solvents/CH3CCl3', 'MC'),
    }

    # Frequency suffix mapping
    SUFFIX = {'pairs': 'All', 'monthly': 'MM'}

    def __init__(self, prog='Otto'):
        p = prog.lower()
        if p == 'otto':
            self.prog = 'Otto'
        elif p == 'fecd':
            self.prog = 'fECD'
        else:
            self.prog = 'OldGC'

        self.sites = self.PROGRAM_SITES[self.prog]
        # OldGC only has F11, F12, N2O
        if self.prog == 'OldGC':
            self.gases = ['F11', 'F12', 'N2O']
        else:
            self.gases = list(self.GAS_PATHS.keys())

    def urls(self, site, freq='monthly'):
        """Generate URLs for a given site and frequency."""
        # Normalize inputs
        code_site = site.lower() if self.prog == 'Otto' else site.upper()
        freq_key = freq.lower()
        # OldGC only supports monthly
        if self.prog == 'OldGC':
            freq_key = 'monthly'

        suffix = self.SUFFIX[freq_key]
        urls = {}
        for gas in self.gases:
            path, override_code = self.GAS_PATHS[gas]
            # file extension
            ext = 'txt' if self.prog == 'fECD' else 'dat'

            if self.prog == 'fECD':
                # fECD files use NOAAflaskECD naming convention
                urls[gas] = (
                    f"{self.BASE_URL}/{path}/flasks/{self.prog}/{freq_key}/"
                    f"{gas}_{code_site}_NOAAflaskECD_{suffix}.{ext}"
                )
            else:
                file_code = override_code or gas
                urls[gas] = (
                    f"{self.BASE_URL}/{path}/flasks/{self.prog}/{freq_key}/"
                    f"{code_site}_{file_code}_{suffix}.{ext}"
                )
        return urls
