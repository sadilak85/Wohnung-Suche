from driverinteraction import *
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
  filenamekeystr = 'immowelt_'
  _url2open, object_ID_list = functions_sourcewebsite.extract_object_url_ID(webbrowser, filenamekeystr,'expose')

  webbrowser.close()
  #
  totalobj2process = 0
  # Open the objects found after search
  for i in range(len(_url2open)):
    if totalobj2process == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    Obj_immowelt_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_immowelt_ch.launchdriver(_url2open[i])
    #
    # Click on the "Contact to" button
    element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactBroker"]', 3)
    cont = Obj_immowelt_ch.continue2click_element(element2click)
    if cont =='clicked':
      element2click.click()
      time.sleep(2) 
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue

    # Filling the form
    element2click = Obj_immowelt_ch.check2click_element('//*[@id="salutation"]', 3)
    cont = Obj_immowelt_ch.continue2click_element(element2click)
    if cont =='clicked':
      element2click.click()
      time.sleep(2) 
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    try:
      Select(element2click).select_by_visible_text(input_List['Salutation'])
    except:
      print('\n-----> Select manually the title: Herr/Frau\n')
      print("\nAfter finishing, press a key to continue\n")
      while True:
        a = input("\n-----> Press Enter to continue\n")
        if a != []:
          break
    try:
      Obj_immowelt_ch.fill_TextBox('//*[@id="firstname"]', input_List['Firstname'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="lastname"]', input_List['Lastname'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="email"]', input_List['Email'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="tel"]', input_List['Telephone'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="message"]', input_List['Message'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      print("\nAfter finishing, press a key to continue\n")
      while True:
        a = input("\n-----> Press Enter to continue\n")
        if a != []:
          break
    try:
      Obj_immowelt_ch.fill_TextBox('//*[@id="street"]', input_List['Street']+' '+input_List['Housenumber'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="zipcode"]', input_List['PostalCode'])
      Obj_immowelt_ch.fill_TextBox('//*[@id="city"]', input_List['City'])
    except:
      pass

    # Click on the radioboxes under message box
    try:
      element2click = Obj_immowelt_ch.check2click_element('//*[@id="requestMoreInformation"]', 3)
      Obj_immowelt_ch.continue2click_element(element2click)
      element2click.click()
      time.sleep(2)
      element2click = Obj_immowelt_ch.check2click_element('//*[@id="requestCallback"]', 3)
      Obj_immowelt_ch.continue2click_element(element2click)
      element2click.click()
      time.sleep(2)
    except:
      print("\n-----> click the check boxes: 'Infomaterial anfordern' 'Rückruf'\n")
      print("\nAfter finishing, press a key to continue\n")
      while True:
        a = input("\n-----> Press Enter to continue\n")
        if a != []:
          break

    # Submit the Form 
    element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactSend"]', 1, ['visible',None,None])
    element2click2 = Obj_immowelt_ch.check2click_element('//*[@id="btnStepForward"]', 1, ['visible',None,None])
    cont = Obj_immowelt_ch.continue2click_element(element2click)
    cont2 = Obj_immowelt_ch.continue2click_element(element2click2)
    if cont =='clicked' or cont2 =='clicked':
      if cont2 =='clicked':
        element2click2.click() # Weiter Button click
      else:
        # element2click.click()   ###################  Burayi en son comment out yap !! ##################
        time.sleep(5)
      # if any error by sending + After weiter button there is extra form manually to fill:
      element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactSend"]', 1, [None,None,'clickable'])
      while element2click != []:
        print("\n----->Finish filling the page and click send button!\n")
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n...")
          if a != []:
            break
        element2click = Obj_immowelt_ch.check2click_element('//*[@id="btnContactSend"]', 1, [None,None,'clickable'])
        if  element2click == []: # submitted manually
          print("\nSubmitted manually and will save a log file as usual\n")
          pass
      print('......................\n Message is successfully sent;)! \n......................')
      totalobj2process = totalobj2process + 1
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue
  
    # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamekeystr+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immowelt(_url2open[i], filepath)

    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")   
  return True


  # HTML from element with `get_attribute`
  #element = webbrowser.find_element_by_css_selector("#hireme")
  #html = element.get_attribute('innerHTML')
#
#