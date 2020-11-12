# File for importing and reading fits files from TESS mission

import os
from astropy.timeseries import TimeSeries
from astropy.time import Time
import matplotlib.pyplot as plt



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

i = 0			# For counting during testing
all_data = []			# Define list for all timeseries data to be stored in, corresponding to names in lightcurve_list
# Opening fits file with astropy
def openfile():
	global i
	for curve in lightcurve_list:
		i = i+1
		print(i)
		all_data.append(TimeSeries.read('./DATA/raw/'+ curve, format = 'kepler.fits'))
	return all_data

# Open FITS and assign data from it to variable stardata
all_data = openfile()


# Get time and pdcsap_flux from timeseries data
fluxes = []
times = []
def getdata(all_data):
	for entry in all_data:
		times.append(Time(entry['time'], format = 'jd').value)	# Using astropy.time to convert isot to jd time format, use value
		fluxes.append(entry['pdcsap_flux'])
	return fluxes, times

#assign data from FITS to two variables
getdata(all_data)

# Function for plotting each lightcurve to a graph
def plot_all():
	for i in range (0, len(fluxes)):
		plt.plot(times[i], fluxes[i])
		plt.title(lightcurve_list[i])
		plt.savefig('./outputs/testing1_outputs/'+lightcurve_list[i][:(len(lightcurve_list[i])-5)]+'.png')
		plt.close()


plot_all()
