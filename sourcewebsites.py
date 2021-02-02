from wohnungsdataclass import ImmobilienSuche
import webscrape
#
from selenium.webdriver.support.ui import Select
#
import time
import os
import re
import shutil
import pathlib
from pathlib import Path
import os.path
#
#
#import pdb
#pdb.set_trace()
#
currentdir = os.path.dirname(os.path.realpath(__file__))
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
#
def get_objectID(objecturl):
  object_ID = re.search('expose/(.*)?', objecturl)
  if object_ID != None:
    object_ID=object_ID.group(1)
  else:
    object_ID = objecturl.split('expose/')[1]
  return object_ID

def search_files_w_Object_ID(_checkfilenamestr):
  check = False
  for dirpath, dirnames, filenames in os.walk("Output"):
    for filename in [f for f in filenames if _checkfilenamestr in f]:
      check = True
  return check

def wait_objects_loaded(_driver, _urlnamestr):
  _url2open = []
  object_ID_list = []
  while object_ID_list == []:
    for link in _driver.find_elements_by_tag_name('a'):
      objecturl = link.get_attribute("href")
      if objecturl != None:
        if "expose" in objecturl:
          object_ID = get_objectID(objecturl)
          check = search_files_w_Object_ID(_urlnamestr+object_ID)
          if not check:
            if objecturl not in _url2open:
              _url2open.append(objecturl)
            if object_ID not in object_ID_list:
              object_ID_list.append(object_ID)
    time.sleep(5)
  return _url2open, object_ID_list


def _immobilienscout24(input_List):
  unformatted_url = 'https://www.immobilienscout24.de/Suche/de/{l}/wohnung-mieten?numberofrooms={r}.0-&price=-{p}.0&livingspace={q}.0-&pricetype=rentpermonth&sorting=2'
  url2open = unformatted_url.format(l=input_List['SearchLocation'], r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'])
  #
  Obj_immobilienscout24 = ImmobilienSuche(input_List)
  webbrowser = Obj_immobilienscout24.launchdriver(url2open)
  #
  #webbrowser.implicitly_wait(10)
  #
  Obj_immobilienscout24.scroll_down()
  #
  _url2open, object_ID_list = wait_objects_loaded(webbrowser, 'Immobilienscout24_')
  #
  #Obj_immobilienscout24.save_cookies()
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    Obj_immobilienscout24_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_immobilienscout24_ch.launchdriver(_url2open[i])
    time.sleep(2) # ## #

    #Obj_immobilienscout24_ch.load_cookies()

    # Click on the "Contact to" button 
    #button = webbrowser2focus.find_element_by_xpath('//*[@id="is24-expose-contact-bar-top"]')
    #webbrowser2focus.implicitly_wait(10)
    #ActionChains(webbrowser2focus).move_to_element(button).click(button).perform()

    element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-expose-contact-bar-top"]')
   
    if element2click != []:
      try:
        element2click.click()
      except:
        print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
        return False     
    else:
      print("Button for 'Contact' is not clickable, the process is aborting...")
      return False

    # Filling the form ### below must be implemented
    select_salutation = Obj_immobilienscout24_ch.check2click_element('//*[@id="salutation"]')
    try:
      Select(select_salutation).select_by_visible_text('Herr')
      # Select(webbrowser2focus.find_element_by_xpath('//*[@id="salutation"]')).select_by_visible_text('Herr')
    except Exception as err:
      print(err)
      return False

    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="firstname"]', input_List['Firstname'])
    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="lastname"]', input_List['Lastname'])
    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="email"]', input_List['Email'])
    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="tel"]', input_List['Telephone'])

    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="message"]', input_List['Message'])

    # submit button ? 

    # extract the page info into log file
    filepath = os.path.join(outdirsession, 'Info_Immowelt_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)
    
    #Obj_immobilienscout24_ch.save_cookies()
    webbrowser2focus.close()

  return True

def _immowelt(input_List):
  unformatted_url = 'https://www.immowelt.de/liste/{l}/wohnungen/mieten?roomi={r}&prima={p}&wflmi={q}&sort=createdate%2Bdesc'
  url2open = unformatted_url.format(l=input_List['SearchLocation'].split('/')[1], r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'])
  #
  Obj_immowelt = ImmobilienSuche(input_List)
  webbrowser = Obj_immowelt.launchdriver(url2open)
  #time.sleep(3)
  #Obj_immowelt.load_cookies()
  Obj_immowelt.scroll_down()
  #
  #
  _url2open, object_ID_list = wait_objects_loaded(webbrowser, 'Immowelt_')

  #Obj_immowelt.save_cookies()
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    Obj_immowelt_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_immowelt_ch.launchdriver(_url2open[i])
    time.sleep(8) # increase here

    #Obj_immowelt_ch.load_cookies()

    # Click on the "Contact to" button
    element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactBroker"]')    ######?? working????
    if element2click != []:
      try:
        element2click.click()
      except:
        print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
        return False   
    else:
      print("Button for 'Contact' is not clickable, the process is aborting...")
      return False

    # Filling the form
    select_salutation = Obj_immowelt_ch.check2click_element('//*[@id="salutation"]')
    try:
      Select(select_salutation).select_by_visible_text('Herr')
      # Select(webbrowser2focus.find_element_by_xpath('//*[@id="salutation"]')).select_by_visible_text('Herr')
    except Exception as err:
      print(err)
      return False

    Obj_immowelt_ch.fill_TextBox('//*[@id="firstname"]', input_List['Firstname'])
    Obj_immowelt_ch.fill_TextBox('//*[@id="lastname"]', input_List['Lastname'])
    Obj_immowelt_ch.fill_TextBox('//*[@id="email"]', input_List['Email'])
    Obj_immowelt_ch.fill_TextBox('//*[@id="tel"]', input_List['Telephone'])

    Obj_immowelt_ch.fill_TextBox('//*[@id="message"]', input_List['Message'])

    # submit button ? 

    # extract the page info into log file
    filepath = os.path.join(outdirsession, 'Info_Immowelt_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)

    
    #Obj_immowelt_ch.save_cookies()
    webbrowser2focus.close()
  return True  

def _immobilienmarkt_sueddeutsche(input_List):
  unformatted_url = 'https://immobilienmarkt.sueddeutsche.de/index.php?action=immo/suchen/trliste/home#&atype=a&pTo={p}&aFrom={q}&rFrom={r}&reg={l}&offset=0&sort=-time'
  url2open = unformatted_url.format(  l = 'DEU091620000001' if input_List['SearchLocation'] == 'bayern/muenchen' 
                                          else 'DEU120000000001' if input_List['SearchLocation'] == 'berlin/berlin' 
                                          else 'DEU020000000001' if input_List['SearchLocation'] == 'hamburg/hamburg'
                                          else 'DEU053150000001' if input_List['SearchLocation'] == 'nordrhein-westfalen/koeln'
                                          else 'DEU060000000001' if input_List['SearchLocation'] == 'hessen/frankfurt-am-main'
                                          else 'DEU081110000001' if input_List['SearchLocation'] == 'baden-wuerttemberg/stuttgart'
                                          else 'DEU064120000001' if input_List['SearchLocation'] == 'nordrhein-westfalen/duesseldorf'
                                          else 'DEU091620000001', r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'])

  Obj_sueddeutsche = ImmobilienSuche(input_List)
  webbrowser = Obj_sueddeutsche.launchdriver(url2open)
  #Obj_sueddeutsche.load_cookies()
  #Obj_sueddeutsche.scroll_down()
  #
  # Open the objects found after search

  xpath = "//div[contains(@class, 'hitHeadline')]"

  element2click_list = webbrowser.find_elements_by_xpath(xpath)
  max_elts = len(element2click_list)

  for i in range(max_elts-1):
    element2click_list = webbrowser.find_elements_by_xpath(xpath)
    try:
      if element2click_list[i].is_displayed():
        element2click_list[i].click()
        Obj_sueddeutsche.scroll_down()
        object_ID = webbrowser.find_element_by_class_name('exposeId').find_element_by_xpath('.//span').get_attribute('textContent')
        _filenamestr = 'Info_Immobilienmarkt_sueddeutsche_'+object_ID
        if not search_files_w_Object_ID(_filenamestr):
          # extract the page info into log file
          filepath = os.path.join(outdirsession, _filenamestr+'.log')
          webscrape.gather_log_info_immobilienmarkt_sueddeutsche('http://immo.sz.de/'+object_ID, filepath)        
          # fill in the contact formular
          Obj_sueddeutsche.fill_TextBox('//*[@id="idDRfirstname"]', input_List['Firstname'])
          Obj_sueddeutsche.fill_TextBox('//*[@id="idDRlastname"]', input_List['Lastname'])
          Obj_sueddeutsche.fill_TextBox('//*[@id="idDRfrom"]', input_List['Email'])
          Obj_sueddeutsche.fill_TextBox('//*[@id="idDRphone"]', input_List['Telephone'])
          Obj_sueddeutsche.fill_TextBox('//*[@id="idDRSenderZusatz"]', input_List['Message'])
          #click radio buttons
          webbrowser.find_element_by_xpath('//*[@id="idDRSenderInfo"]').click()
          webbrowser.find_element_by_xpath('//*[@id="idDRSenderTermin"]').click()
          webbrowser.find_element_by_xpath('//*[@id="idDRSenderCall"]').click()
          # click on submit button
          submitbutton = webbrowser.find_element_by_xpath('//*[@id="directReqShort"]')
          #submitbutton.click()  # are you sure now?

          
        webbrowser.execute_script("window.history.go(-1)")
    except:
      pass

  #Obj_sueddeutsche_ch.save_cookies()
  webbrowser.close()
  return True  

  #  _input.send_keys(Keys.ENTER)
  #webbrowser.get('https://www.seleniumeasy.com/')
  #assert 'Selenium Easy' in webbrowser.title

  # HTML from element with `get_attribute`
  #element = webbrowser.find_element_by_css_selector("#hireme")
  #html = element.get_attribute('innerHTML')
#