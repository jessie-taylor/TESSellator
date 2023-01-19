import pandas as pd
import lightkurve as lk
from lightkurve.periodogram import LombScarglePeriodogram

# Getting the first 11 columns, as it imports 12 with the last one being blank 
csv = pd.read_csv('./KEBCv3.csv', header=7, usecols=[i for i in range(11)])

# For the list of the #KICS, use csv['#KIC']

skippedlist = []
# Copied from obtaining_skarka_data.py
# TESTING - WILL OUTPUT LK PERIODOGRAMS OF STARS - can be modified later so it saves them
for star in csv["#KIC"]:
  print ("\nSearching for star", star)
  try:
    print(lk.search_lightcurve("TIC" + str(star), exptime = 1800, author = "TESS-SPOC")) #seeing which sectors are available)
    lc = lk.search_lightcurve("TIC" + str(star), exptime = 1800, author = "TESS-SPOC"
                        ).download(  # changed to download_all for experimenting with stitching
#                        ).stitch(        # putting multiple together
                        ).remove_nans()
    LombScarglePeriodogram.from_lightcurve(lc).plot() # Should add nyquist_factor arg
    plt.ylim(0,500) # Setting y limits to same as used with Kepler data
    plt.tick_params(axis = 'both', which = 'both', direction = 'out') # Moving ticks to outside of plot
    plt.savefig("./eb_periodograms_delete_later/" + str(star) + ".png")
    lc.plot()    # INSERT LINE HERE FOR PLOTTING THE LC BEFORE DFT
    plt.savefig("./eb_periodograms_delete_later/" + str(star) + "_lc.png")
  except AttributeError:  # Error handling if no data available, as the download fn will output AttributeError
    print("Skipped star", star)
    skippedlist.append(star)

# Print total number of stars and those skipped due to no available data
print( "\nTotal stars searched for:", len(csv["Name"]), "\nTotal skipped:", len(skippedlist))
