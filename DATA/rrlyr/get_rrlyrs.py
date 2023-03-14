import rrlyr.parse_drakeedit as parse
import lightkurve as lk
from astroquery.simbad import Simbad
import astropy.units as u
import astropy.coordinates as coord
from rrlyr.TICer import any_TICer
import csv

# Scripted to be imported from parent directory as module
# This already returns TIC IDs, so no need to TICer after

# First import all type-ab RR Lyrae stars
def get_abs():
  # Drake (2013) only states coordinates of targets
  # So using these to try find star IDs
  # Define list for ids to enter
  dirtytics = []
  tics = []
  ids = []
  table = parse.df_from_file("./rrlyr/from_drake.txt")
  for i in range (0, len(table)):
    print ("on", str(i) + "/" + str(len(table)))
    radeg = table["RAdeg"][i]
    dedeg = table["DEdeg"][i]
    # Get main ID for target (will be a weird one, these stars are old)
    find_star = Simbad.query_region(coord.SkyCoord(radeg, dedeg,
                                                   unit = (u.deg, u.deg)),
				                   radius = "0d0m2s")
    # Get ID from returned array
    # In try/except because some will return None
    try:
      # Extra index as it's in a little array
      ids.append(find_star["MAIN_ID"][0])
    except TypeError:
      continue
  
  # Now send to any_TICer
  # Which is a version of TICer for non-KIC ID input
  for star in ids:
    if star != None:
      # dirtytics as some will return None and need cleaning up
      # Using index 0 to obtain string
      dirtytics.append(any_TICer(star))
    else:
      continue
  
  # Clean up to remove Nones
  for star in dirtytics:
    if star != None:
      tics.append(star)
    else:
      continue

  return tics

# For RR Lyrae type-c TICS
def get_rrcs():
  # Obtain TICs from benko data
  rrctics = []
  # Open CSV file
  with open("./rrlyr/from_benko_2023.txt") as csvfile:
    # skipinitialspace as inconsistent numbers of spaces
    reader = csv.reader(csvfile, skipinitialspace = True, delimiter = " ")
    for row in reader:
      # [-1] index as TICs are last entry on each row
      rrctics.append(row[-1])
  return rrctics
