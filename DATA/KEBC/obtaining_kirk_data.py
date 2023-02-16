import pandas as pd
import lightkurve as lk
from lightkurve.periodogram import LombScarglePeriodogram
from TICer import TICer
import matplotlib.pyplot as plt
from time import sleep

# Getting the first 11 columns, as it imports 12 with the last one being blank 
csv = pd.read_csv('./KEBCv3.csv', header=7, usecols=[i for i in range(11)])

skippedlist = []
# Copied from obtaining_skarka_data.py
# TESTING - WILL OUTPUT LK PERIODOGRAMS OF STARS
# can be modified later so it saves them
for star in csv["#KIC"]:
  kicid = str(star)
  # Obtain TIC from KIC
  # With exception for if timeout occurs
  try:
    star = TICer(str(star))
  except ConnectionError:
    # Wait 30 seconds and retry request
    print ("Timeout from Simbad, waiting 30 seconds and retrying")
    sleep(30)
    star = TICer(str(star))
  print ("\nSearching for star TIC", star, ", KIC", kicid)
  try:
    # See which sectors are available
    print(lk.search_lightcurve("TIC" + str(star), 
                                exptime = 1800, 
                                author = "TESS-SPOC"))
    lc = lk.search_lightcurve("TIC" + str(star), 
                               exptime = 1800, 
                               author = "TESS-SPOC"
                        ).download(  # changed to download_all for stitching
#                        ).stitch(        # putting multiple together
                        ).remove_nans()
    # Can add nyquist_factor arg to this if needed
    LombScarglePeriodogram.from_lightcurve(lc).plot()
    # Setting y limits to same as used with Kepler data
    plt.ylim(0,500)
    # Moving ticks to outside of plot
    plt.tick_params(axis = 'both', which = 'both', direction = 'out')
    plt.savefig("./eb_periodograms_delete_later/" + str(star) + ".png")
    lc.plot()
    # Plotting pre-DFT LC
    plt.savefig("./eb_periodograms_delete_later/" + str(star) + "_lc.png")
    plt.close()
  # Error handling if no data available
  # as the download function will output AttributeError
  except AttributeError:
    if star == None:
      print("Skipped star KIC ", kicid)
      skippedlist.append("KIC " + kicid)
    else:
      print("Skipped star", star)
      skippedlist.append(star)

# Print total number of stars and those skipped due to no available data
print( "\nTotal stars searched for:", len(csv["Name"]), 
       "\nTotal skipped:", len(skippedlist))

