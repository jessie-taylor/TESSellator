# Module version made to be run with arraymaker
import pandas as pd
from KEBC.TICer import TICer
from time import sleep

#              ~   ~
#           ~         ~
#        ~               ~
#     ~                    ~
#  ~                          ~
# ~ ~ ~ ~ Module version ~ ~ ~ ~ #
def murphy_dsct():
  """
  Provides TIC IDs for the stars within the dsct catalogue
  from Murphy et al. 2019. 
   
  Yields
  ------
  Python list of TIC IDs of catalogue
  """
  dsct_tic_list = []
  file = open("./dsct_murphy/murphy_manclasses_just_KICS.txt")
  raw_kics = file.readlines()
  file.close()
  # Stripping "\n" from the ends of lines
  dsct_kics = []
  for kic in raw_kics:
    if kic[-1:] == "\n":
      kic = kic[:-1]
    dsct_kics.append(kic)
  
  for star in dsct_kics:
    # Obtain TIC from KIC
    # With exception for if timeout occurs
    try:
      star = TICer(str(star))
    except ConnectionError:
      # Wait 30 seconds and retry request
      print ("Timeout from Simbad, waiting 30 seconds and retrying")
      sleep(30)
      star = TICer(str(star))
    dsct_tic_list.append(star)
  return dsct_tic_list
