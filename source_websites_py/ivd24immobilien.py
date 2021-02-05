from wohnungsdataclass import ImmobilienSuche
import functions_sourcewebsite
import webscrape
#
from selenium.webdriver.support.ui import Select
#
import time
import os
import os.path
#
#
#import pdb
#pdb.set_trace()
#
def _ivd24immobilien(input_List):
  Obj_ivd24immobilien = ImmobilienSuche(input_List)
  webbrowser = Obj_ivd24immobilien.launchdriver('https://www.ivd24immobilien.de/')

  select = webbrowser.find_element_by_xpath("//div[contains(@class, 'SumoSelect sumo_anzahl_zimmer')]")
  select.click()

  if int(input_List['TotalRooms'])<3:
    select = webbrowser.find_element_by_xpath('//*[@id="search-form"]/div/div[4]/div/div/ul/li[2]')
    select.click()
  elif int(input_List['TotalRooms'])<4:
    select = webbrowser.find_element_by_xpath('//*[@id="search-form"]/div/div[4]/div/div/ul/li[3]')
    select.click()
  else:
    select = webbrowser.find_element_by_xpath('//*[@id="search-form"]/div/div[4]/div/div/ul/li[4]')
    select.click()

  Obj_ivd24immobilien.fill_TextBox('//*[@id="search-form"]/div/div[5]/input', input_List['Budget'])
  Obj_ivd24immobilien.fill_TextBox('//*[@id="search-form"]/div/div[6]/input', input_List['SurfaceArea'])

  #Obj_ivd24immobilien.fill_TextBox('//*[@id="photon_ortschaft"]', input_List['SearchLocation'].split('/')[1])
  #webbrowser.find_element_by_xpath('//*[@id="ui-id-1"]').click()
  
  element = webbrowser.find_element_by_xpath('//input[contains(@placeholder, "Wo | Ort, Stadtteil, PLZ, Objekt-ID")]')
  element.send_keys(input_List['SearchLocation'].split('/')[1])

  webbrowser.find_element_by_xpath("//span[contains(@class, 'ac-label') and text()='München']").click()

  element2click = Obj_ivd24immobilien.check2click_element('//*[@id="search-submit"]')
  cont = Obj_ivd24immobilien.cont_clicked_element (element2click)
  if cont =='error':
    return False
  else:
    webbrowser.close()
    time.sleep(2)      


  time.sleep(10)
  return True