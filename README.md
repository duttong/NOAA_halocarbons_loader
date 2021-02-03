<h3>NOAA Global Monitoring Laboratory (GML) Halocarbon data loader</h3>
  
<p>Methods for loading NOAA/GML halocarbon data from the NOAA/GML FTP site located at: ftp://ftp.cmdl.noaa.gov/hats</p>

<p>There are several measurement programs for halocarbon data. The loader method in the class HATS_Loader will return monthly mean flask data measured on the M3 mass spectrometer instrument. To select data from a different measurement program use the 'program' key word. Valid flask measurement programs include 'M3', 'otto', 'oldgc'. Use 'CATS' or 'RITS' for in situ measurements.</p>

<p>The 'freq' key word is short for measurement frequence. All programs return monthly means or medians. 'freq' can be set to 'daily' or 'hourly' for the in situ measurement programs.</p>

<p>The loader returns a Pandas multi-index dataframe where the index are a three letter site code and the measesurement date. Columns returned are dry mole fraction in parts-per-trillion (ppt) (except for N2O which is in parts-per-billion) and one standard deviation of the mean of air measurements. Columns are denoted as 'mf' for mole fraction and 'sd' for standard deviation.</p>

<p>Examples:

```
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
