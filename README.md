<h2>NOAA Global Monitoring Laboratory (GML) Halocarbons (and a few other gases) Data Loader</h2>

<p>Methods for loading NOAA/GML halocarbon data from the NOAA/GML FTP site located at: ftp://ftp.cmdl.noaa.gov/hats</p>

<p>The current list of gases avaiable are: C2Cl4, C2H2, C2H6, C3H8, CCl4, CF4, CH2Cl2, CH3Br, CH3CCl3, CH3Cl, F11, F113,
 F114, F115, F12, F13, HCFC123, HCFC124, HCFC133a, HCFC141b, HCFC142b, HCFC22, HFC125, HFC134a, HFC143a, HFC152a, HFC227ea,
 HFC236fa, HFC32, HFC365mfc, HFO1234yf, HFO1234ze, N2O, NF3, OCS, PFC116, PFC218, SF6, SO2F2, h1211, h1301, h2402,
 i-butane, i-pentane, n-butane, n-hexane, n-pentane</p>
  
<p>There are several measurement programs for halocarbon data. The loader method in the class HATS_Loader will return monthly mean flask data measured on the M3 mass spectrometer instrument. To select data from a different measurement program use the 'program' key word. Valid flask measurement programs include 'M3', 'otto', 'oldgc'. Use 'CATS' or 'RITS' for in situ measurements.</p>

<p>The 'freq' key word is short for measurement frequence. All programs return monthly means or medians. 'freq' can be set to 'daily' or 'hourly' for the in situ measurement programs.</p>

<p>The loader returns a Pandas multi-index dataframe where the index are a three letter site code and the measesurement date. Columns returned are dry mole fraction in parts-per-trillion (ppt) (except for N2O which is in parts-per-billion) and one standard deviation of the mean of air measurements. Columns are denoted as 'mf' for mole fraction and 'sd' for standard deviation.</p>

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
                         mf      sd
site date                          
alt  2010-04-01  240.780000  0.3400
     2010-05-01  241.050000  0.3575
     2010-06-01  240.670000  0.2275
     2010-07-01  239.495000  0.4150
     2010-08-01  239.425000  0.2525
...                     ...     ...
thd  2018-11-01  229.883333  0.0700
     2018-12-01  229.498000  0.0900
     2019-01-01  229.053333  0.1300
     2019-02-01  228.860000  0.1650
     2019-03-01  228.695000  0.0700

[1536 rows x 2 columns]
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
