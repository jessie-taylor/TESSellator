# File for importing and reading fits files from TESS mission

# open file and read contents
def openfile():
	print("Please enter file name you would like to open")
	filename = input()
	rawdata = open(filename, "r")
	print (rawdata)


openfile()
