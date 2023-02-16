# Module version of obtaining_kirk_data.py made to be run with arraymaker
import pandas as pd
import lightkurve as lk
from lightkurve.periodogram import LombScarglePeriodogram
from TICer import TICer
import matplotlib.pyplot as plt
from time import sleep

#              ~   ~
#           ~         ~
#        ~               ~
#     ~                    ~
#  ~                          ~
# ~ ~ ~ ~ Module version ~ ~ ~ ~ #
def ebs():
  """
  Uses the Kepler Eclipsing Binary Catalog to obtain lightcurves of 
  EB stars identified in V3 of the KEBC.
  Performs DFT on light curves before 
  
  Yields
  ------
  Python list of TIC IDs of KEBC
  """
  eb_tic_list = []
  # Getting the first 11 columns of the KEBCv3,
  # as it imports 12 with the last one being blank 
  csv = pd.read_csv('./KEBCv3.csv', 
                    header=7, 
                    usecols=[i for i in range(11)])
  
  for star in csv["#KIC"]:
    # Obtain TIC from KIC
    # With exception for if timeout occurs
    try:
      star = TICer(str(star))
    except ConnectionError:
      # Wait 30 seconds and retry request
      print ("Timeout from Simbad, waiting 30 seconds and retrying")
      sleep(30)
      star = TICer(str(star))
    eb_tic_list.append(star)
  return eb_tic_list
