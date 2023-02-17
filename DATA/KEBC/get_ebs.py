# Module version of obtaining_kirk_data.py made to be run with arraymaker
import pandas as pd
from KEBC.TICer import TICer
from time import sleep

#              ~   ~
#           ~         ~
#        ~               ~
#     ~                    ~
#  ~                          ~
# ~ ~ ~ ~ Module version ~ ~ ~ ~ #
def ebs():
  """
  Provides TIC IDs for the stars within the KEBC V3.
   
  Yields
  ------
  Python list of TIC IDs of KEBC
  """
  eb_tic_list = []
  # Getting the first 11 columns of the KEBCv3,
  # as it imports 12 with the last one being blank 
  csv = pd.read_csv('./KEBC/KEBCv3.csv', 
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
