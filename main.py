#
import source_websites_py.immobilienscout24
import source_websites_py.immowelt
import source_websites_py.immobilienmarkt_sueddeutsche
import source_websites_py.ivd24immobilien
import source_websites_py.null_provision
import source_websites_py.immonet
#
import re
import os
import os.path
import time
import shutil
import pathlib
from pathlib import Path
#
#import pdb
#pdb.set_trace()
#

TITLE = '''


█░█░█ █▀█ █░█ █▄░█ █░█ █▄░█ █▀▀   █▀ █░█ █▀▀ █░█ █▀▀
▀▄▀▄▀ █▄█ █▀█ █░▀█ █▄█ █░▀█ █▄█   ▄█ █▄█ █▄▄ █▀█ ██▄


'''

# Paths:
currentdir = os.path.dirname(os.path.realpath(__file__))
UserDataInput = Path(currentdir) / 'UserInputs' / 'UserDataInput.txt'
MessageFile = Path(currentdir) / 'UserInputs' / 'message.txt'
PostalCodeFile = Path(currentdir) / 'UserInputs' / 'PostalCodesDE.txt'

outdir = Path(currentdir) / "Output"
if not os.path.exists(outdir):
    os.mkdir(outdir)

try:
	for folder in list(os.walk(outdir))[1:]:
		if not folder[2]:
			shutil.rmtree(folder[0], ignore_errors=True) # Delete the empty folders in <outdir> directory
except:
	pass

outdirsession = Path(outdir) / time.strftime("%Y%m%d-%H%M%S")
os.mkdir(outdirsession)

input_List = {'Browsertype': 'Chrome', # Browsers: ['Ie', 'Chrome', 'Firefox'] or more.. must be setted first
              'Message': [],
              'Sourceweb' : [],
              'Salutation': [],
              'Firstname': [],
              'Lastname': [],
              'Email': [],
              'Telephone': [],
              'Street': [],
              'Housenumber': [],
              'PostalCode': [],
              'City': [],
              'SearchLocation': 'bayern/muenchen',
              'Budget': [],
              'TotalRooms': [],
              'SurfaceArea': [],
              'MaxObj2Search': [],
              'ChromeUserProfilePath': [],
              'Outputdirectory': outdirsession
}

  
def check_positive_integer(num):
  try:
    val = int(num)
    if val <= 0:  # if not a positive int print message and ask for input again
      print("Sorry, input must be a positive integer and not zero, try again")
      return False
    return True
  except ValueError:
    print("That's not an integer!")
    return False

def check_PLZ(num):
  with open(PostalCodeFile, mode='r') as infile:
    lines = [line.rstrip() for line in infile]
    for line in lines:
      if num == line:
        return True
  return False

def main():
  print('-------------------------------------------------')
  print(TITLE)
  print('-------------------------------------------------')
  #
  # Message file check!!!
  try:
    filename = open(MessageFile, "r")
    input_List['Message'] = filename.read()
    filename.close()
  except:
    print("Input file error: Check if file named 'UserDataInput.txt' available in ./UserInputs folder")
  #
  #
  with open(UserDataInput, mode='r', encoding="utf-8") as infile:
    lines = [line.rstrip() for line in infile]
    for line in lines:
      try:
        input_List['Salutation'] = line.split('Salutation>>',1)[1].strip()
      except:
        pass 
      try:
        input_List['Firstname'] = line.split('Firstname>>',1)[1].strip()
      except:
        pass
      try:
        input_List['Lastname'] = line.split('Lastname>>',1)[1].strip()
      except:
        pass
      try:
        input_List['Email'] = line.split('Email>>',1)[1].strip()
      except:
        pass
      try:
        input_List['Telephone'] = line.split('Telephone>>',1)[1].strip()
      except:
        pass
      try:
        input_List['Street'] = line.split('Street>>',1)[1].strip()
      except:
        pass
      try:
        input_List['Housenumber'] = line.split('Housenumber>>',1)[1].strip()
      except:
        pass
      try:
        input_List['PostalCode'] = line.split('PostalCode>>',1)[1].strip()
      except:
        pass
      try:
        input_List['City'] = line.split('City>>',1)[1].strip()
      except:
        pass
      try:
        input_List['SearchLocation'] = line.split('SearchLocation>>',1)[1].strip()
      except:
        pass
      try:
        input_List['Budget'] = line.split('Budget>>',1)[1].strip()
      except:
        pass
      try:
        input_List['TotalRooms'] = line.split('TotalRooms>>',1)[1].strip()
      except:
        pass
      try:
        input_List['SurfaceArea'] = line.split('SurfaceArea>>',1)[1].strip()
      except:
        pass
      try:
        input_List['ChromeUserProfilePath'] = line.split('ChromeUserProfilePath>>',1)[1].strip()
      except:
        pass
      try:
        input_List['Browsertype'] = line.split('Browsertype>>',1)[1].strip()
      except:
        pass
      try:
        input_List['MaxObj2Search'] = line.split('MaxObj2Search>>',1)[1].strip()
      except:
        pass        
  #
  if len(input_List['Firstname'])<=2:
    print('You must enter a name longer than 2 letters...')
    print('You entered: '+input_List['Firstname'])
    print('Now aborting...')
    quit()
  if len(input_List['Lastname'])<=2:
    print('You must enter a name longer than 2 letters...')
    print('You entered: '+input_List['Lastname'])
    print('Now aborting...')
    quit()  
  if not check_positive_integer(input_List['Telephone']):
    print('Telephone number entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['Telephone'])
    print('Now aborting...')
    quit()
  if not check_positive_integer(input_List['Housenumber']):
    print('House number entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['Housenumber'])
    print('Now aborting...')
    quit()
  if not check_positive_integer(input_List['Budget']):
    print('Budget entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['Budget'])
    print('Now aborting...')
    quit()
  if not check_positive_integer(input_List['TotalRooms']):
    print('Number of rooms entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['TotalRooms'])
    print('Now aborting...')
    quit()
  if not check_positive_integer(input_List['SurfaceArea']):
    print('Surface area entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['SurfaceArea'])
    print('Now aborting...')
    quit()
  if not check_positive_integer(input_List['MaxObj2Search']):
    print('Max object to search entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['MaxObj2Search'])
    print('Now aborting...')
    quit()          
  if not check_PLZ(input_List['PostalCode'] ):
    print('Post number (PLZ) entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['PostalCode'])
    print('Now aborting...')
    quit()
  if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", input_List['Email']):
    print('Email entry in User Input File is incorrect, please correct it and then restart...')
    print('You have entered: '+input_List['Email'])
    print('Now aborting...')
    quit()
  # 
  index = input_List['Salutation']
  if index == 'H':
    input_List['Salutation'] = 'Herr'
  elif index == 'F':
    input_List['Salutation'] = 'Frau'
  else:
    print('Default Salutation <Herr> is selected!')
  #
  index = input_List['Browsertype']
  if index == 'C':
    input_List['Browsertype'] = 'Chrome'
  elif index == 'F':
    input_List['Browsertype'] = 'Firefox'
  elif index == 'I':
    input_List['Browsertype'] = 'Ie'
  else:
    print('Default Browser <Chrome> is selected!')
  #
  index = input_List['SearchLocation']
  if index == 'M':
    input_List['SearchLocation'] = 'bayern/muenchen'
  elif index == 'B':
    input_List['SearchLocation'] = 'berlin/berlin'
  elif index == 'H':
    input_List['SearchLocation'] = 'hamburg/hamburg'
  elif index == 'K':
    input_List['SearchLocation'] = 'nordrhein-westfalen/koeln'
  elif index == 'F':
    input_List['SearchLocation'] = 'hessen/frankfurt-am-main'
  elif index == 'S':
    input_List['SearchLocation'] = 'baden-wuerttemberg/stuttgart'
  elif index == 'D':
    input_List['SearchLocation'] = 'nordrhein-westfalen/duesseldorf'
  else:
    print('Default City <Muenchen> is selected!')
  #
  #SourceWebSites_List = ['immowelt', 'immobilienscout24', 'null_provision', 'immobilienmarkt_sueddeutsche', 'ivd24immobilien', 'immonet']
  SourceWebSites_List = ['immonet']
  #
  for i, _webstr in enumerate(SourceWebSites_List):
    input_List['Sourceweb'] = _webstr
    print('......................\nInitializing for {}.de \n......................'.format(_webstr))
    if eval("source_websites_py."+ "{s}._{s}".format(s=_webstr) + "(input_List)"):
      print("......................\nProcess for {} is finished.\n......................".format(_webstr))
    else:
      print("......................\n Process for {} ended with some errors!\n......................".format(_webstr))
      #quit()
#
if __name__ == '__main__':
    main()
#