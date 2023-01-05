# Script for obtaining Skarka data
# This will need to be able to read the table
# and separate out the gdor and dsct files
# Generate a list of the stars
# And download the data from LK

import parse
import lightkurve as lk
from lightkurve.periodogram import LombScarglePeriodogram
import matplotlib.pyplot as plt

table5 = parse.df_from_file("table5_classifications.dat")


# Function for getting lists of desired type
def get_list(classification):
  return table5[table5["VType"] == classification]
  
# Calling function to obtain dfs of only desired classications
gdordf = get_list("GDOR")
dsctdf = get_list("DSCT")

skippedlist = [] #list of stars which had no suitable data

# Loop exists just so I can see which pipelines are available for stars at a quick look
#for star in gdordf["Name"]:
#  # run each one through LK
#  print ("doing this for star", star)
#  try:
#    print(lk.search_lightcurve("TIC" + str(star),
#                        exptime = 1800)) # Need to specify author for correct S.C. data
#  except:
#    print("Skipped", star, "due to lack of data")
#    skippedlist.append(star)


# TESTING - WILL OUTPUT LK PERIODOGRAMS OF STARS - can be modified later so it saves them
for star in gdordf["Name"]:
  print ("Searching for star", star)
  try:
    print(lk.search_lightcurve("TIC" + str(star), exptime = 1800)) #seeing which sectors are available)
    lc = lk.search_lightcurve("TIC" + str(star), exptime = 1800
                        ).download_all(  # changed to download_all for experimenting with stitching
                        ).stitch(        # putting multiple together
                        ).remove_nans()
    LombScarglePeriodogram.from_lightcurve(lc, ny).plot() # Creating LSP from data before and plotting
    plt.show()
  except:
    print("Skipped star", star)
    skippedlist.append(star)
