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

def remove_empty_folders(removefolderpath):
	try:
		for folder in list(os.walk(removefolderpath))[1:]:
			if not folder[2]:
				shutil.rmtree(folder[0], ignore_errors=True) # Delete the empty folders in removefolderpath directory
	except:
		pass

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
  _url2open = []
  object_ID_list = []
  while object_ID_list == []:
    for link in webbrowser.find_elements_by_tag_name('a'):
      objecturl = link.get_attribute("href")
      if objecturl != None:
        if "expose" in objecturl:
          object_ID = get_objectID(objecturl)
          check = False
          for dirpath, dirnames, filenames in os.walk("Output"):
            for filename in [f for f in filenames if 'Immobilienscout24_'+object_ID in f]:
              check = True
          if not check:
            _url2open.append(objecturl)
            object_ID_list.append(object_ID)
    time.sleep(10)

  print(object_ID_list)

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
    element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-expose-contact-bar-top"]', 'clickable')
    #element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="btnContactBroker"]', 'visible')
    #element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="btnContactBroker"]', 'present')
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
    select_salutation = Obj_immobilienscout24_ch.check2click_element('//*[@id="salutation"]', 'visible')
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

    filepath = os.path.join(outdirsession, 'Info_Immowelt_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)
    remove_empty_folders(outdir)
    
    time.sleep(3)
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
  _url2open = []
  object_ID_list = []
  for link in webbrowser.find_elements_by_tag_name('a'):
    objecturl = link.get_attribute("href")
    if objecturl != None:
      if "expose" in objecturl:
        object_ID = get_objectID(objecturl)
        check = False
        for dirpath, dirnames, filenames in os.walk("Output"):
          for filename in [f for f in filenames if 'Immowelt_'+object_ID in f]:
            check = True
        if not check:
          _url2open.append(objecturl)
          object_ID_list.append(object_ID)
  
  print(object_ID_list)

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
    element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactBroker"]', 'clickable')
    #element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactBroker"]', 'visible')
    #element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactBroker"]', 'present')
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
    select_salutation = Obj_immowelt_ch.check2click_element('//*[@id="salutation"]', 'visible')
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

    filepath = os.path.join(outdirsession, 'Info_Immowelt_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)
    remove_empty_folders(outdir)
    
    time.sleep(3)
    #Obj_immowelt_ch.save_cookies()
    webbrowser2focus.close()
  return True  

def _immobilienmarkt_sueddeutsche(input_List):
  pass


  #  _input.send_keys(Keys.ENTER)
  #webbrowser.get('https://www.seleniumeasy.com/')

  #searchbox = webbrowser.find_element_by_id('edit-search-block-form--2')
  #searchbox.clear()
  #searchbox.send_keys('python')

  #assert 'Selenium Easy' in webbrowser.title
  #click_searchbox = webbrowser.find_element_by_xpath('//*[@id="search-block-form"]/div/div/div[1]/span/button')
  #click_searchbox.click()

  #assert 'Date pickers' in webbrowser.page_source


  #html = webbrowser.page_source
  # HTML from `<html>`
  #html = webbrowser.execute_script("return document.documentElement.innerHTML;")

  # HTML from `<body>`
  #html = webbrowser.execute_script("return document.body.innerHTML;")

  # HTML from element with some JavaScript
  #element = webbrowser.find_element_by_css_selector("#hireme")
  #html = webbrowser.execute_script("return arguments[0].innerHTML;", element)

  # HTML from element with `get_attribute`
  #element = webbrowser.find_element_by_css_selector("#hireme")
  #html = element.get_attribute('innerHTML')
#

#  _input.send_keys(Keys.ENTER)