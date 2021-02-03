<p>Methods for loading NOAA/GML halocarbon data from the NOAA/GML FTP site
located at: ftp://ftp.cmdl.noaa.gov/hats</p>

<p>There are several measurement programs for halocarbon data. The loader
method in the class HATS_Loader will return monthly mean flask data
measured on the M3 mass spectrometer instrument. To select data from a
different measurement program use the 'prog' key word. Valid flask measurement
programs include 'M3', 'otto', 'oldgc'. Use 'CATS' or 'RITS' for in situ
measurements.</p>

<p>The 'freq' key word is short for measurement frequence. All programs return
monthly means or medians. 'freq' can be set to 'daily' or 'hourly' for the
in situ measurement programs.</p>
