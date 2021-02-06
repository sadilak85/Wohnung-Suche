from driverinteraction import ImmobilienSuche
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
  Obj_immowelt.scroll_down()
  #
  #
  filenamekeystr = 'Immowelt_'
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, filenamekeystr,'expose')

  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    if i == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    Obj_immowelt_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_immowelt_ch.launchdriver(_url2open[i])
    #Obj_immowelt_ch.load_cookies()
    #
    # Click on the "Contact to" button
    element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactBroker"]')
    cont = Obj_immowelt_ch.cont_clicked_element (element2click)
    if cont =='clicked':
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue

    # Filling the form
    select_salutation = Obj_immowelt_ch.check2click_element('//*[@id="salutation"]')
    cont = Obj_immowelt_ch.cont_clicked_element (select_salutation)
    if cont =='clicked':
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    try:
      Select(select_salutation).select_by_visible_text(input_List['Salutation'])
    except:
      print('\n-----> Select manually the title: Herr/Frau\n')
      time.sleep(10)
      pass
    try:
      Obj_immowelt_ch.fill_TextBox('//*[@id="firstname"]', input_List['Firstname'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="lastname"]', input_List['Lastname'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="email"]', input_List['Email'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="tel"]', input_List['Telephone'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="message"]', input_List['Message'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      time.sleep(10)

    # Click on the radioboxes under message box
    try:
      Obj_immowelt_ch.cont_clicked_element (Obj_immowelt_ch.check2click_element('//*[@id="requestMoreInformation"]'))
      Obj_immowelt_ch.cont_clicked_element (Obj_immowelt_ch.check2click_element('//*[@id="requestCallback"]'))
    except:
      print("\n-----> click the check boxes: 'Infomaterial anfordern' 'Rückruf'\n")
      time.sleep(10)
      pass

    #submit here
  
    # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamekeystr+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)

    #Obj_immowelt_ch.save_cookies()
    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")   
  return True


  #  _input.send_keys(Keys.ENTER)
  #webbrowser.get('https://www.seleniumeasy.com/')
  #assert 'Selenium Easy' in webbrowser.title

  # HTML from element with `get_attribute`
  #element = webbrowser.find_element_by_css_selector("#hireme")
  #html = element.get_attribute('innerHTML')
#
#