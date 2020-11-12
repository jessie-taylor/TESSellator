# File for importing and reading fits files from TESS mission

import os
from astropy.timeseries import TimeSeries


#Create list of files in ./data/raw/ and return list of variables
# Will need to get rid of non-FITS files

#define variables
lightcurve_list = []

def dirscan():
	dir_contents_list = os.listdir('./data/raw')
	for line in dir_contents_list:
		if line[(len(line)-4):] == 'fits':
			lightcurve_list.append(line)
	with open('./outputs/lc_list.txt', 'w') as f:	#Write list to file, ./outputs/lc_list.txt
		for item in lightcurve_list:
			f.write('%s\n' % item)

dirscan()

num = 0 				#FOR COUNTING WITH TESTING
# Opening fits files with astropy
def openfile():
	for item in lightcurve_list:
		global num
		num= num+1
		print (num)
		ts = TimeSeries.read('./DATA/raw/' + item, format = 'kepler.fits')
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
