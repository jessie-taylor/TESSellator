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

# New version, which uses the lists which have been manually reviewed
def nvs():
  nvs = []
  # Just turn these np arrays to regular lists
  nvs1 = np.load("./skarka/reviewed_nvs/nvs_keep_1000.npy")
  nvs2 = np.load("./skarka/reviewed_nvs/nvs_keep_2000.npy")
  for star in nvs1:
    nvs.append(str(star))
  for star in nvs2:
    nvs.append(str(star))

  return nvs

# Old version, deprecated
def nvs_old():
  table5 = parse.df_from_file("./skarka/table5_classifications.dat")
  
  # Non-variables come up as VType == None in the dataframe
  # so need to be handled differently
  nvs = []
  for n in range (0, len(table5)):
    if table5.iloc[n]["VType"] == None:
      name = table5.iloc[n]["Name"].item()
      nvs.append(str(name))
  
  return nvs
