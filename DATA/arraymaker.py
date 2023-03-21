# Rewriting for TESS data in 2023
from KEBC.get_ebs import ebs
from get_dfts import get_dfts
from skarka.get_gdor_dsct import gdor, dsct, nvs
from rrlyr.get_rrlyrs import get_abs, get_rrcs

import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from datetime import datetime
import lightkurve as lk
from os import path, listdir
from os.path import isfile, join
 

# function for getting dfts from get_dfts
# and putting them in arrays
# Made as a function so it can be called for each of the catalogues
def make_array(ids: list, catname: str):
  """
  Uses lists of IDs generated from catalog modules
  to obtain DFTs, and plot those to generate arrays
  for use in a CNN.

  Parameters
  ----------
  ids : list
      List of TIC IDs, generated by individual catalog modules.
      Must be added as only numbers, no "TIC" preamble.
      TIC ID expected as str.
  catname : str
      Name of catalog ids is associated with.
      This determines the filename of generated array.

  Yields
  ------
  complete_array : np.array                      [MIGHT BE WRONG HERE - CHECK]
      Numpy array generated and saved with name
      corresponding to catname input string.
  """
  namearray = []
  completearray = np.empty([480, 640, 0])
  total_i = 0
  i = 0

  # Remove ids that come up as None using a filter
  print ("Removing Nones from list. Length of list before filtering:", 
         len(ids))
  idsfiltered = filter(lambda item: item is not None, ids)
  ids = list(idsfiltered)
  print ("Nones removed, new length of TIC ID list:", len(ids))

  # Check to see if arrays already exist for this set
  # This is blind to the number contained in the arrays,
  # ie if the arrays represent all available data
  # Setting variable answer so it can be used before setting
  answer = None
  filelist= [f for f in listdir("./arrays/") if isfile(join("./arrays", f))]
  for f in filelist:
    if f[:(len(catname))] == catname and answer == None:
      print ("\nArrays already exist for the class", catname)
      print ("Would you like to continue anyway (overwriting previous)? y/n")
      answer = input()
  if answer == "n":
    return None
        
	

  # obtain DFTs from list of IDs
  stars_data = get_dfts(ids)
  
  # Using each ID to loop through each star in the dictionary
  # [ might want to add an exception if no data was found 
  # but see where the error pops up first
  for starid in ids:
    print('On star', total_i, '/', len(ids))
    # Get the time now, for seeing how long each iteration takes
    timehere = datetime.now()

    # Try/Except in case no dft available for star
    try:
      # Obtain the dft for this star
      dft = stars_data[str(starid) + "_dft"]
    # If no DFT available
    except KeyError:
      print ("Skipped", starid, "due to no available LC data")
      continue
    
    # Add name to namearray for keeping track of which star is which
    namearray.append(starid)

    # for plotting, can get frequency with dft.frequency
    # can also obtain period and power the same way 
    plt.plot(dft.frequency, dft.power)
    plt.ylim(-1, 500)
    plt.savefig("arraymakingplot_deleteaftercomplete.png")
    
    # Add image to array
    imagearray = Image.open('arraymakingplot_deleteaftercomplete.png')
    image2 =imagearray.convert('L')
    arrayappender =np.asarray(image2, dtype="int32")
    completearray =np.dstack((arrayappender, completearray))
    plt.clf()

    # Counting total number for recording
    i = i + 1
    total_i = total_i + 1

    # Save array if it gets to 1000 entries, to avoid memory issues
    if i == 1000:
      # Naming array with which stars it contains
      arrayname = "arrays/" + catname + "_" + str(total_i) + ".npy"
      # Save array of plots
      np.save(arrayname, completearray)
      # Save array of names
      np.save(arrayname[:-4] + '_names.npy', namearray)
      # Clear array ready for next 1000
      completearray = np.empty([480, 640, 0])
      namearray = []
      # Reset to keep track of how many are in next array
      i = 0
    # To keep track of how long things take - print time taken
    print('time to complete loop =', datetime.now()-timehere)
    
  print(completearray.shape)
  np.save('arrays/' 
          + catname 
	  + '_' 
	  + str(total_i) 
	  + '.npy', completearray) #save remaining files
  np.save('arrays/' 
          + catname 
	  + '_' 
	  + str(total_i) 
	  + '_names.npy', namearray)  # ADDED FOR NAMING
  print(len(namearray))

 
# Call on make_array to build arrays for each category
# for each one of the catalogs

# Obtain list of EB TICs 
eb_ids = ebs()
# Build array of ebs
make_array(eb_ids, "ebs")

# Obtain list of gdor and dsct
gdor_ids = gdor()
make_array(gdor_ids, "gdor")

dsct_ids = dsct()
make_array(dsct_ids, "dsct")

# see how it works with using both type a, b, and c at once (only 2 abs)
rrlyr_ids = get_abs + get_rrcs
make_array(rrlyr_ids, "rrlyr")

nvids = nvs()
make_array(nvids, "nv")


# EXTRA INFO IS IN lc.meta, such as the TEFF etc, which will be useful later
# It's a dictionary, so can use lc.meta["TEFF"] etc
# This info is also still retained in the dft

