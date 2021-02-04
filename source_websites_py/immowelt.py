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
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, 'Immowelt_','expose')

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
    cont = functions_sourcewebsite.cont_clicked_element (element2click)
    if cont =='clicked':
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue

    # Filling the form
    select_salutation = Obj_immowelt_ch.check2click_element('//*[@id="salutation"]')
    cont = functions_sourcewebsite.cont_clicked_element (select_salutation)
    if cont =='clicked':
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    try:
      Select(select_salutation).select_by_visible_text('Herr')
      # Select(webbrowser2focus.find_element_by_xpath('//*[@id="salutation"]')).select_by_visible_text('Herr')
    except Exception as err:
      print(err)
      print('Select manually the title: Herr/Frau')
      time.sleep(10)
      pass

    Obj_immowelt_ch.fill_TextBox('//*[@id="firstname"]', input_List['Firstname'])
    Obj_immowelt_ch.fill_TextBox('//*[@id="lastname"]', input_List['Lastname'])
    Obj_immowelt_ch.fill_TextBox('//*[@id="email"]', input_List['Email'])
    Obj_immowelt_ch.fill_TextBox('//*[@id="tel"]', input_List['Telephone'])

    Obj_immowelt_ch.fill_TextBox('//*[@id="message"]', input_List['Message'])

     # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_Immowelt_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)

    #Obj_immowelt_ch.save_cookies()
    webbrowser2focus.close()
  return True


  #  _input.send_keys(Keys.ENTER)
  #webbrowser.get('https://www.seleniumeasy.com/')
  #assert 'Selenium Easy' in webbrowser.title

  # HTML from element with `get_attribute`
  #element = webbrowser.find_element_by_css_selector("#hireme")
  #html = element.get_attribute('innerHTML')
#
#