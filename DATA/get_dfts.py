# Module that takes TIC ID lists, searches for and downloads the data, 
# then outputs a dataframe of the IDs and DFT data (not plotted) 
# to be used by arraymaker.
# Will be called upon by arraymaker and only take a list of strings of TIC IDs
# as input.
# The majority of this code can be taken from obtaining_kirk_data.py
import pandas as pd
import lightkurve as lk
from time import sleep
from lightkurve.periodogram import LombScarglePeriodogram

def get_dfts(ids: list):
  """
  Take description from above and make it fancy and nice
  """
  skippedlist = []
  # Creating dictionary which will be used as output
  # format will be [star_name]_lc for lightcurve
  # and [star_name]_dft for dft
  stars_data = {}

  for star in ids:
    # altered version of what's in obtaining_kirk_data.py ~~~~~~~~~~~~~~~~~~~~~
    #                                           ~~~~~~~~ edited it line by line
    #                                                             they dared me
    #                                                             bet i couldnt
    #                                                                  dared me
    try:
      # See which sectors are available
      # and download them (or first available if download_all not used)
      # With error handling if timeout
      try: 
        print(lk.search_lightcurve("TIC" + str(star), 
                                    exptime = 1800, 
                                    author = "TESS-SPOC"))
        lc = lk.search_lightcurve("TIC" + str(star), 
                                   exptime = 1800, 
                                   author = "TESS-SPOC"
                            ).download(  # change to download_all for stitching
#                            ).stitch(        # putting multiple together
                            ).remove_nans()
      except (ConnectionError): # Removed specifying ConnectionError: as it was failing strangely
        print ("Timeout from Simbad, waiting 60 seconds and retrying")
        sleep(60)
        print(lk.search_lightcurve("TIC" + str(star), 
                                    exptime = 1800, 
                                    author = "TESS-SPOC"))
        lc = lk.search_lightcurve("TIC" + str(star), 
                                   exptime = 1800, 
                                   author = "TESS-SPOC"
                            ).download(  # change to download_all for stitching
#                            ).stitch(        # putting multiple together
                            ).remove_nans()
      # Perform DFT
      # Can add nyquist_factor arg to this if needed
      dft = LombScarglePeriodogram.from_lightcurve(lc)

      # Add lc and dft to dictionary
      stars_data[str(star + "_lc")] = lc
      stars_data[str(star + "_dft")] = dft

      # Error handling if no data available
    # as the download function will output AttributeError
    except AttributeError:
      if star == None:
        continue
      else:
        print("Skipped star", star)
        skippedlist.append(star)
  # Print total number of stars and those skipped due to no available data
  print( "\nTotal stars searched for:", len(ids), 
         "\nTotal skipped:", len(skippedlist))

  return stars_data
