# unused - use version in Colab
# https://colab.research.google.com/drive/1I7w3v5C6tkun8IpHGFGejLL3DpHSLuFT?usp=sharing
import numpy as np
from PIL import Image

test_image_data = np.load("./model/test_image_data.npy")
predictions_array = np.load("./model/predictions.npy", allow_pickle = True)


