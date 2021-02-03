from wohnungsdataclass import ImmobilienSuche
import webscrape
#
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
#
import time
import os
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
def get_objectID(objecturl, _keystr):
  try:
    object_ID = objecturl.split(_keystr+'/')[1].split('?')[0]
  except:
    object_ID = None
  return object_ID

def search_files_w_Object_ID(_checkfilenamestr):
  check = False
  for dirpath, dirnames, filenames in os.walk("Output"):
    for filename in [f for f in filenames if _checkfilenamestr in f]:
      check = True
  return check

def wait_objects_loaded(_driver, _urlnamestr, _keystr):
  _url2open = []
  object_ID_list = []
  while object_ID_list == []:
    for link in _driver.find_elements_by_tag_name('a'):
      objecturl = link.get_attribute("href")
      if objecturl != None:
        if _keystr in objecturl:
          object_ID = get_objectID(objecturl, _keystr)
          check = search_files_w_Object_ID(_urlnamestr+object_ID)
          if not check:
            if objecturl not in _url2open:
              _url2open.append(objecturl)
            if object_ID not in object_ID_list:
              object_ID_list.append(object_ID)
    time.sleep(5)
  return _url2open, object_ID_list

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
  _url2open, object_ID_list = wait_objects_loaded(webbrowser, 'Immowelt_','expose')

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

     # extract the page info into log file
    filepath = os.path.join(outdirsession, 'Info_Immowelt_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)

    #Obj_immowelt_ch.save_cookies()
    webbrowser2focus.close()
  return True

def _immobilienscout24(input_List):
  unformatted_url = 'https://www.immobilienscout24.de/Suche/de/{l}/wohnung-mieten?numberofrooms={r}.0-&price=-{p}.0&livingspace={q}.0-&pricetype=rentpermonth&sorting=2'
  url2open = unformatted_url.format(l=input_List['SearchLocation'], r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'])
  #
  Obj_immobilienscout24 = ImmobilienSuche(input_List)
  webbrowser = Obj_immobilienscout24.launchdriver(url2open)
  #
  #webbrowser.implicitly_wait(10)
  #
  # Captcha !!! get rid of this manually!
  while 'Robot' in webbrowser.title:
    print('waiting from user to get rid of Captcha manually to continue')
    time.sleep(15)
      
  Obj_immobilienscout24.scroll_down()
  #
  _url2open, object_ID_list = wait_objects_loaded(webbrowser, 'Immobilienscout24_', 'expose')
  #
  #Obj_immobilienscout24.save_cookies()
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    Obj_immobilienscout24_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_immobilienscout24_ch.launchdriver(_url2open[i])
    time.sleep(2) # ## #

    webbrowser2focus.execute_script("window.scrollTo(0, window.scrollY + 1500)")
    time.sleep(2)

    element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-sticky-contact-area"]/div[1]/div/div[2]/a/span[1]')
    if element2click != []:
      try:
        element2click.click()
        time.sleep(2)
      except:
        print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
        return False     
    else:
      print("Button for 'Contact' is not clickable, skipping this task...")
      webbrowser2focus.close()
      time.sleep(2)
      continue

    # Filling the form
    select_salutation = Obj_immobilienscout24_ch.check2click_element('//*[@id="contactForm-salutation"]')
    if select_salutation != []:
      try:
        select_salutation.click()
        time.sleep(2)
      except:
        print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
        return False     
    else:
      print("Button for 'Contact' is not clickable, skipping this task...")
      webbrowser2focus.close()
      time.sleep(2)
      continue
    try:
      Select(select_salutation).select_by_visible_text('Herr')
    except Exception as err:
      print(err)
      pass

    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-Message"]', input_List['Message'])
    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-firstName"]', input_List['Firstname'])
    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-lastName"]', input_List['Lastname'])
    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-emailAddress"]', input_List['Email'])
    Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-phoneNumber"]', input_List['Telephone'])
    try:
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-street"]', input_List['Street'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-houseNumber"]', input_List['Housenumber'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-postcode"]', input_List['PostalCode'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-city"]', input_List['City'])
    except:
      pass


    # submit button ?  weiter:  some of them has this option
    # //*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[5]/div/button/span

    # last send button:
    # //*[@id="is24-expose-modal"]/div/div/div/div/div[1]/div/div/div/form/div[5]/button

    while True:
      print(webbrowser.find_element_by_xpath('//*[@id="expose-title"]').text)
      time.sleep(5)
    quit()

    # extract the page info into log file
    filepath = os.path.join(outdirsession, 'Immobilienscout24_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immobilienscout24(webbrowser2focus, filepath)
    
    webbrowser2focus.close()
  return True

def _null_provision(input_List):
  unformatted_url = 'https://www.null-provision.de/mietwohnung,{l}.html?price={p}_euro&rooms=ab-{r}-zimmer&area=ab-{q}-qm&order=neueste'
  url2open = unformatted_url.format(l=input_List['SearchLocation'],
                                    r = '5' if int(input_List['TotalRooms']) > 5 else input_List['TotalRooms'],
                                    p='bis_200' if int(input_List['Budget']) <= 200 
                                    else 'bis_400' if int(input_List['Budget']) <= 400
                                    else 'bis_600' if int(input_List['Budget']) <= 600
                                    else 'bis_800' if int(input_List['Budget']) <= 800
                                    else 'bis_1000' if int(input_List['Budget']) <= 1000
                                    else 'bis_1250' if int(input_List['Budget']) <= 1250
                                    else 'bis_1500' if int(input_List['Budget']) <= 1500
                                    else 'bis_1750' if int(input_List['Budget']) <= 1750
                                    else 'ab_1750' , 
                                    q='40' if int(input_List['SurfaceArea']) < 60
                                    else '60' if int(input_List['SurfaceArea']) < 80
                                    else '80' if int(input_List['SurfaceArea']) < 100
                                    else '100' if int(input_List['SurfaceArea']) < 120
                                    else '120' if int(input_List['SurfaceArea']) < 140
                                    else '140' if int(input_List['SurfaceArea']) < 160
                                    else '160' if int(input_List['SurfaceArea']) < 180
                                    else '180' if int(input_List['SurfaceArea']) < 200
                                    else '200' )
  #
  Obj_null_provision = ImmobilienSuche(input_List)
  webbrowser = Obj_null_provision.launchdriver(url2open)
  #
  _url2open, object_ID_list = wait_objects_loaded(webbrowser, 'null_provision_', 'angebot')
  #Obj_immobilienscout24.save_cookies()
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    _url2open[i] = _url2open[i].replace('https://www.null-provision.de/angebot/','https://www.immobilienscout24.de/expose/')
    Obj_null_provision_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_null_provision_ch.launchdriver(_url2open[i])
    time.sleep(2) #

    # Captcha !!! get rid of this shit manually first!
    while 'Robot' in webbrowser2focus.title:
      print('waiting from user to get rid of Captcha manually to continue')
      time.sleep(15)

    webbrowser2focus.execute_script("window.scrollTo(0, window.scrollY + 1500)")
    time.sleep(2)

    element2click = Obj_null_provision_ch.check2click_element('//*[@id="is24-sticky-contact-area"]/div[1]/div/div[2]/a/span[1]')
    if element2click != []:
      try:
        element2click.click()
        time.sleep(2)
      except:
        print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
        return False     
    else:
      print("Button for 'Contact' is not clickable, skipping this task...")
      webbrowser2focus.close()
      time.sleep(2)
      continue

    # Filling the form
    select_salutation = Obj_null_provision_ch.check2click_element('//*[@id="contactForm-salutation"]')
    if select_salutation != []:
      try:
        select_salutation.click()
        time.sleep(2)
      except:
        print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
        return False     
    else:
      print("Button for 'Contact' is not clickable, skipping this task...")
      webbrowser2focus.close()
      time.sleep(2)
      continue    
    try:
      Select(select_salutation).select_by_visible_text('Herr')
    except Exception as err:
      print(err)
      pass

    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-firstName"]', input_List['Firstname'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-lastName"]', input_List['Lastname'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-emailAddress"]', input_List['Email'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-phoneNumber"]', input_List['Telephone'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-street"]', input_List['Street'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-houseNumber"]', input_List['Housenumber'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-postcode"]', input_List['PostalCode'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-city"]', input_List['City'])
    Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-Message"]', input_List['Message'])

    # submit button ?

    # extract the page info into log file
    filepath = os.path.join(outdirsession, 'null_provision_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immobilienscout24(webbrowser2focus, filepath)
    
    webbrowser2focus.close()
  return True

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
  if element2click != []:
    try:
      element2click.click()
    except:
      print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
      return False     
  else:
    print("Button for 'Contact' is not clickable, the process is aborting...")
    return False

  time.sleep(10)
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
#