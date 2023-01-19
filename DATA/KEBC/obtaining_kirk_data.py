import pandas as pd

# Getting the first 11 columns, as it imports 12 with the last one being blank 
csv = pd.read_csv('./KEBCv3.csv', header=7, usecols=[i for i in range(11)])

# For the list of the #KICS, use csv['#KIC']
