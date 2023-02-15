# Now requires a subdirectory in scripts dir named OutputArrays
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from datetime import datetime
CompleteArray =np.empty([480, 640, 0])
NameArray = []  # ADDED FOR NAMING
total_i = 0
dir = 'binaries_training_set/'
for subdirectories, dirs, files in os.walk(dir):
  i = 0
  for subdir in dirs:
    try:
      print('On file', total_i, '/', len(dirs))
      i = i + 1
      total_i = total_i + 1 #counting total number for recording
      timehere = datetime.now() # getting time now
      spectra = np.loadtxt(dir+subdir+'/s000000.dat')
      NameArray.append(subdir[:-18]) # ADDED FOR NAMING
      plt.plot(spectra[:, 0], spectra[:, 1])
      if (np.max(spectra[:,1]) <=500):
        plt.ylim(0,500)
      plt.savefig('graph.png')
      ImageArray = Image.open('graph.png')
      image2 =ImageArray.convert('L')
      ArrayAppender =np.asarray(image2, dtype="int32")
      CompleteArray =np.dstack((ArrayAppender, CompleteArray))
      plt.clf()
    except:
      pass
    if i == 1000:
      #naming array with which i it goes to from the last
      arrayname = 'OutputArrays/' + dir[:-1] + '_' + str(total_i) + '.npy'       
      np.save(arrayname, CompleteArray) #save array every 1000 files
      np.save(arrayname[:-4] + '_names.npy', NameArray)  # ADDED FOR NAMING
      CompleteArray = np.empty([480, 640, 0]) #clear array that's just been saved
      NameArray = [] # Clearing naming array
      i = 0 #reset number to 0
    print('time to complete loop =', datetime.now()-timehere) #print time to loop
    
print(CompleteArray.shape)
np.save('OutputArrays/' + dir[:-1] + '_' + str(total_i) + '.npy', CompleteArray) #save remaining files
np.save('OutputArrays/' + dir[:-1] + '_' + str(total_i) + '_names.npy', NameArray)  # ADDED FOR NAMING

# Rewriting for TESS data in 2023
# Keep all import stuff from above (lines 2 - 6)
from KEBC import obtaining_kirk_data_module as kebc

CompleteArray = np.empty([480, 640, 0])
NameArray = []
total_i = 0
# First, gather the lightcurves using the kebc module
# Put them into arrays using the method from the original version of arraymaker
# Save arrays in ./arrays

