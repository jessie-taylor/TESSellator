# Small module for import from arraymaker
import skarka.parse as parse

def gdor():
  table5 = parse.df_from_file("./skarka/table5_classifications.dat")

  # Function for getting lists of desired type
  def get_list(classification):
    return table5[table5["VType"] == classification]
  
  # Calling function to obtain dfs of only desired classications
  gdordf = get_list("GDOR")

  # Create list and put TIC IDs in list
  gdors = []
  for tic in gdordf["Name"]:
    gdors.append(str(tic))

  return gdors

def dsct():
  table5 = parse.df_from_file("./skarka/table5_classifications.dat")

  # Function for getting lists of desired type
  def get_list(classification):
    return table5[table5["VType"] == classification]
  
  # Calling function to obtain dfs of only desired classications
  dsctdf = get_list("DSCT")
  
  # Create list and put TIC IDs in list
  dscts = []
  for tic in dsctdf["Name"]:
    dscts.append(str(tic))

  return dscts
