# Program for loading and running trained model saved by other code
# Saves output files in directory [kepmags]predictions_plotted/

import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from os import walk
from os import mkdir
from datetime import datetime

# Obtaining list of files in array directory (both iamgearrays and names)
arraydir = './TestOutputArrays/'
dirarrays = next(walk(arraydir), (None, None, []))[2]

# Separate the arrays into names and image arrays
data_orig_path = []
names_path = []
for filename in dirarrays: # Creating arrays of the file paths/names
  if filename[-9:] == 'names.npy':
    names_path.append(arraydir + filename)
  else:
    data_orig_path.append(arraydir + filename)

# Loading in pretrained model
model = tf.keras.models.load_model('./saved_classifier_model')

def run_model(array):
  # Import data and put all in one array
  data_together = np.empty((480,640,0), dtype='float64')
  timehere = datetime.now()

  data_together = np.concatenate((data_together, np.load(array)), axis=2)
  print('\nTime to concatenate =', datetime.now()-timehere)
  # COMMENTED OUT BECAUSE NOT APPLICABLE TO SETS WHERE... 
  # ...THE NAMES ARE ALL IN ONE ARRAY ALREADY.
  # SHOULD BE UNCOMMENTED IF THEY NEED PUTTING TOGETHER
  names_together = np.empty((0), dtype='<U13')
  namepath = array[:-4] + '_names.npy'  # defining path to corresponding name array
  names_together = np.concatenate((names_together, list(reversed(np.load(namepath)))))


  # Preparing data for the CNN
  data1 = np.transpose(data_together, (2,0,1))
  data1 = data1.reshape(-1, 480, 640, 1)
  data1 = data1.astype('float32')
  data1 = data1 / 255.

  # Make predictions and save them to variable predictions
  predictions = model.predict(data1)

  # Output graphs with labels in filename
  classification_labels = ['nv', 'gd', 'ds', 'hyb']

  for i in range(0, len(data1)): 
    Image.fromarray(np.transpose(data_together, (2,0,1))[i]).convert('RGB').save(
          arraydir[:6] + '_predictions_plotted/'
          + classification_labels[np.argmax(predictions[i])]
          + '_'
          + names_together[i]
          + '.png')

# Creating directory for output, unless it already exists
try:
  mkdir(arraydir[:6] + '_predictions_plotted/')
except OSError:
  pass


# Running model across each of the available arrays
i = 1
for array in data_orig_path:
  print(f'Running on array {i} of {len(data_orig_path)}')
  run_model(array)  #run_model being the name of the function to be defined above
  i = i + 1
