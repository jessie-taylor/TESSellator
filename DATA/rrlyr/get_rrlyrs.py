import parse_drakeedit as parse
import lightkurve as lk
from astroquery.simbad import Simbad
import astropy.units as u
import astropy.coordinates as coord
from TICer import any_TICer

# Change into module format after testing
# This already returns TIC IDs, so no need to TICer after

# First import all type-ab RR Lyrae stars
def get_abs():
  # Drake (2013) only states coordinates of targets
  # So using these to try find star IDs
  # Define list for ids to enter
  tics = []
  ids = []
  table = parse.df_from_file("from_drake.txt")
  for i in range (0, len(table)):
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

  # Now find useable IDs using a modified TICer:
  # send the IDs as strings to any_TICer
  # First take each elem out of masked array into plain string
  
  # Now send to any_TICer
  for star in ids:
    tics.append(any_TICer(star[0])
  

  return tics

