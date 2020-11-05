# File for importing and reading fits files from TESS mission

from astropy.timeseries import TimeSeries


# Opening fits file with astropy
def openfile():
	ts = TimeSeries.read('./DATA/raw/tess2018206045859-s0001-0000000029829699-0120-s_lc.fits', format = 'kepler.fits')
	return ts

# Open FITS and assign data from it to variable stardata
stardata = openfile()


# Get time and pdcsap_flux from timeseries data
def getdata(file):
	timecorr = file['timecorr']
	pdcsap_flux = file['pdcsap_flux']
	return timecorr, pdcsap_flux

#assign data from FITS to two variables
timecorr, pdcsap_flux = getdata(stardata)
print (timecorr), print (pdcsap_flux)
