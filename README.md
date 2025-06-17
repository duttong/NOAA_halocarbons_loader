<h1>NOAA Global Monitoring Laboratory (GML) Halocarbons (and a few other gases) Data Loader</h1>

<p>Simple methods for loading NOAA/GML halocarbon data from the NOAA/GML FTP site located at: https://gml.noaa.gov/aftp/data/hats/</p>

<p>The current list of gases available are: C2Cl4, C2H2, C2H6, C3H8, CCl4, CF4, CH2Cl2, CH3Br, CH3CCl3, CH3Cl, F11, F113,
 F114, F115, F12, F13, HCFC123, HCFC124, HCFC133a, HCFC141b, HCFC142b, HCFC22, HFC125, HFC134a, HFC143a, HFC152a, HFC227ea,
 HFC236fa, HFC32, HFC365mfc, HFO1234yf, HFO1234ze, N2O, NF3, OCS, PFC116, PFC218, SF6, SO2F2, h1211, h1301, h2402,
 i-butane, i-pentane, n-butane, n-hexane, n-pentane</p>

<p>The example below shows how to use the loader method. The following keywords are available: program, freq, gapfill, and addlocation</p>

<h3>program</h3>
<p>There are several measurement programs for halocarbon data. The loader method in the class HATS_Loader will return monthly mean flask data measured on the M3 mass spectrometer instrument. To select data from a different measurement program use the <strong>program</strong> keyword. Valid flask measurement programs include 'M3', 'otto', 'oldgc'. Use 'CATS' or 'RITS' for in situ measurement programs. The 'combined' or 'combo' program can be used for the following gases: N2O, SF6, F11, F12, F113, CCl4.</p>

<h3>freq</h3>
<p>The <strong>freq</strong> keyword is short for measurement frequency. All programs return monthly means or medians. 'freq' can be set to 'daily' or 'hourly' for the in situ measurement programs.</p>

<h3>gapfill</h3>
<p>When the gapfill keyword is set to True and the frequency of data (freq keyword) is 'monthly', a seasonally interpolation is done to fill any missing data. Any missing data in the mole fraction ('mf') are filled in with a seasonal gap fill model. The 
model results are returned in 'mf_mod'. The data is also extended 12 months with a model forecast.</p>

<h3>addlocation</h3>
<p>By default, latitude, longitude, and sample elevation are added to the dataframe. Set
addlocation to False to exclude these fields.</p>

<p>The loader returns a Python Pandas multi-index dataframe where the index is a three letter site code and the measurement date. Columns returned are dry mole fraction in parts-per-trillion (ppt) (except for N2O which is in parts-per-billion) and one standard deviation of the mean of air measurements. Columns are denoted as 'mf' for mole fraction and 'sd' for standard deviation.</p>

<h3>Igor Pro Halocarbons Loader</h3>
<p>The <strong>HATS FTP Data.ipf</strong> file are Igor Pro functions to load data from the GML FTP site. They are similar to the Python functions but do not have gap fill methods.</p>

<h3>Examples:</h3>

```python
import pandas as pd

import halocarbons_loader
hats = halocarbons_loader.HATS_Loader()
df = hats.loader('F11')

Loading data for F11
File URL: ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/flasks/GCMS/CFC11b_GCMS_flask.txt
Please consult the header in the file listed above for PI and contact information.
>>> df
                         mf      sd      lat       lon   elev
site date                                                    
alt  2010-04-01  240.780000  0.3400  82.4508  -62.5072  185.0
     2010-05-01  241.050000  0.3575  82.4508  -62.5072  185.0
     2010-06-01  240.670000  0.2275  82.4508  -62.5072  185.0
     2010-07-01  239.495000  0.4150  82.4508  -62.5072  185.0
     2010-08-01  239.425000  0.2525  82.4508  -62.5072  185.0
...                     ...     ...      ...       ...    ...
thd  2020-06-01  224.972500  0.2575  41.0541 -124.1510  107.0
     2020-07-01  224.785000  0.1850  41.0541 -124.1510  107.0
     2020-08-01  224.355000  0.1225  41.0541 -124.1510  107.0
     2020-09-01  223.883333  0.1000  41.0541 -124.1510  107.0
     2020-10-01  224.330000  0.0750  41.0541 -124.1510  107.0

[1799 rows x 5 columns]
```

<h3>To load in situ data from the CATS program try:</h3>

```python
import halocarbons_loader
hats = halocarbons_loader.HATS_Loader()

df = hats.loader('F11', program='CATS')
Loading data for F11
File URL: ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/CATS/monthly/brw_F11_MM.dat
File URL: ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/CATS/monthly/nwr_F11_MM.dat
File URL: ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/CATS/monthly/mlo_F11_MM.dat
File URL: ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/CATS/monthly/smo_F11_MM.dat
File URL: ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/CATS/monthly/spo_F11_MM.dat
File URL: ftp://ftp.cmdl.noaa.gov/hats/cfcs/cfc11/insituGCs/CATS/monthly/sum_F11_MM.dat
Please consult the header in the files listed above for PI and contact information.
```

<h3>Working with Pandas multi-index.</h3>

```python
import pandas as pd
import matplotlib.pyplot as plt

df['mf']['brw'].plot()
df['mf']['spo'].plot()
plt.show()

# or use the cross section method (xs)
df.xs('brw').mf.plot()
plt.show()
```


<h3>Disclaimer</h3>
<p>This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.</p>
