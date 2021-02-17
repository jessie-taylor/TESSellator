# File for importing and reading fits files from TESS mission
import os
from astropy.timeseries import TimeSeries
from astropy.time import Time
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import matplotlib.ticker as ticker

#Create list of files in ./data/raw/ and return list of variables
# Will need to get rid of non-FITS files

print ('If this is being run to create data for ML, comment out line 121')

#define variables
lightcurve_list = []
timecorrection = 2457000

def dirscan():
	dir_contents_list = os.listdir('./data/raw')
	for line in dir_contents_list:
		if line[(len(line)-4):] == 'fits':
			lightcurve_list.append(line)
	#Write list to file, ./outputs/lc_list.txt
	with open('./outputs/lc_list.txt', 'w') as f:	
		for item in lightcurve_list:
			f.write('%s\n' % item)


# Define list for all timeseries data to be stored in
# corresponding to names in lightcurve_list 
all_data = []		
# Opening fits file with astropy
def openfile():
	i = 0
	for curve in lightcurve_list:
		i = i+1
		all_data.append(TimeSeries.read('./DATA/raw/'+ curve,
				format = 'kepler.fits'))
	print (i, "light curves opened")
	return all_data


# Function for removing all data where quality flag is > 0
def quality_prune():
	for n in range(len(all_data)):
		all_data[n] = all_data[n][all_data[n]['quality'] == 0]		

# Fn to rem areas of bad data - set manually after visual inspection of data
# bounds set before calling - allows to be run more than once
def remove_bad(lowerbound, upperbound):
	for i in range (len(all_data)):
		all_data[i] = all_data[i][np.logical_or(
				(all_data[i]['time'].jd-timecorrection) < lowerbound, 
				(all_data[i]['time'].jd-timecorrection) > upperbound)]
	print ('Bad data trimmed (if specified)')


# Get time and pdcsap_flux from timeseries data
def getdata(all_data):
    i = 0
    times = []
    fluxes = []
    for entry in all_data:
	# Using astropy.time to convert isot to jd time
        times.append(Time(entry['time'], format = 'jd').value) 
        fluxes.append(entry['pdcsap_flux'].value)
        i = i+1
    # Now get rid of nan values from data:
    for i in range (len(fluxes)):
        times[i] = times[i][~np.isnan(fluxes[i])]
        fluxes[i] = fluxes[i][~np.isnan(fluxes[i])]
    print (i, 'light curve data preprocessed for DFT')
    return fluxes, times


# Function to get DFT from data
freqs, powers = [],[]       # Defining variables to store DFT values in
from astropy.timeseries import LombScargle
def dft():
    print ('Performing DFTs')
    # To go through all entries in both fluxes and times
    for i in range(0, len(fluxes)):                    
        frequency, power = LombScargle(times[i], 
				fluxes[i]).autopower( 
				method = 'auto', nyquist_factor=None, 
				maximum_frequency=50, minimum_frequency=None)
        freqs.append(frequency)
        powers.append(power)
    print(i, 'DFTs performed')
    return freqs, powers


# Function for plotting each lightcurve to a graph
def plot_all():
	for i in range (0, len(fluxes)):
		fig = plt.figure(figsize=(20,10))
		ax = fig.add_subplot(1,1,1)
		ax.plot(times[i]-timecorrection, fluxes[i], linewidth=0.5)
		ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
		ax.title.set_text(lightcurve_list[i])
		plt.xlabel('Time (JD)')
		plt.ylabel('PDCSAP flux ($e^{-}/s$')
		plt.savefig('./outputs/plots/' 
				+ lightcurve_list[i][:(len(lightcurve_list[i])-5)] 
				+ '.png', 
				bbox_inches = "tight")
		plt.close()


# Function for plotting DFTs to graphs
def plt_dft():
	for i in range(0,len(fluxes)):
		fig = plt.figure(figsize=(20,10))
		ax = fig.add_subplot(1,1,1)
		ax.plot(freqs[i], powers[i], linewidth = 0.5)
		ax.set_ylim([0, 0.2])
		ax.set_xlim([-0.5, 50])
		ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
		ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
		ax.title.set_text('DFT '+lightcurve_list[i]) # comment out
		plt.xlabel('Frequency ($d^{-1}$)')
		plt.ylabel('Power')
		plt.savefig('./outputs/plots/' 
				+ lightcurve_list[i][:(len(lightcurve_list[i])-5)] 
				+ '_DFT.png', 
				bbox_inches = "tight")
		plt.close()
		

# Get plot zoomed in to just one day
def plot_zoomed():
	for i in range (0, len(fluxes)):
		plt.figure(figsize=(20,10))
		plt.plot(times[i][0:719]-timecorrection, fluxes[i][0:719], linewidth=0.8)
		plt.title(lightcurve_list[i])
		plt.xlabel('Time (JD)')
		plt.ylabel('PDCSAP flux ($e^{-}/s$')
		plt.savefig('./outputs/plots/' 
				+ lightcurve_list[i][:(len(lightcurve_list[i])-5)] 
				+ '_zoomed'+'.png',
				 bbox_inches = "tight")
		plt.close()


dirscan()

 # Open FITS and assign data from it to variable stardata
all_data = openfile()

# Prune data
quality_prune()

# assign ranges for removal of large areas of bad data
lowerbound = 0 #1347.35633 
upperbound = 0 #1349.57164
remove_bad(lowerbound, upperbound)

#assign data from FITS to two variables
fluxes, times = getdata(all_data)

dft()
print("Plotting...")
plot_all()
plt_dft()
#plot_zoomed()		
