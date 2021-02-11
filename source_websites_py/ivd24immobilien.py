from driverinteraction import *
import functions_sourcewebsite
import webscrape
#
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
#
import time
import os
import os.path
#
#
import pdb
#pdb.set_trace()
#
def _ivd24immobilien(input_List):
  Obj_ivd24immobilien = ImmobilienSuche(input_List)
  webbrowser = Obj_ivd24immobilien.launchdriver('https://www.ivd24immobilien.de/')
  #
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

  try:
    Obj_ivd24immobilien.fill_TextBox('//*[@id="search-form"]/div/div[5]/input', input_List['Budget'])
    Obj_ivd24immobilien.fill_TextBox('//*[@id="search-form"]/div/div[6]/input', input_List['SurfaceArea'])
  except:
    print('\n-----> Complete the form manually to finish\n')
    print("\nAfter finishing, press a key to continue\n")
    while True:
      a = input("\n-----> Press Enter to continue\n")
      if a != []:
        break

  Obj_ivd24immobilien.fill_TextBox('//*[@id="photon_ortschaft"]', input_List['SearchLocation'].split('/')[1])
  time.sleep(2)
  webbrowser.find_element_by_xpath('//*[@id="ui-id-1"]/li[1]/div').click()

  element2click = Obj_ivd24immobilien.check2click_element('//*[@id="search-submit"]', 3)
  cont = Obj_ivd24immobilien.continue2click_element(element2click)
  if cont =='obscured':
    return False
  elif cont == 'clicked':
    element2click.click()
  else:
    webbrowser.close()
    time.sleep(2)
  #
  # 
  filenamekeystr = 'ivd24immobilien_'
  element2click = Obj_ivd24immobilien.check2click_element('//*[text()="Exposé anzeigen"]', 20, ['visible',None,None])

  _url2open, object_ID_list = functions_sourcewebsite.extract_object_url_ID_ivd24immobilien(webbrowser, filenamekeystr)
  #
  webbrowser.close()
  #
  totalobj2process = 0
  # Open the objects found after search
  for i in range(len(_url2open)):
    if totalobj2process == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    Obj_ivd24immobilien_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_ivd24immobilien_ch.launchdriver(_url2open[i])
    #
    xpath_contact = '//*[@id="expose-anbieter-content"]/div[3]/button'
    # Scroll to contact formular and fill it:  
    ActionChains(webbrowser2focus).move_to_element(webbrowser2focus.find_element_by_xpath(xpath_contact)).perform()
    element2click = Obj_ivd24immobilien_ch.check2click_element(xpath_contact, 3)
    cont = Obj_ivd24immobilien_ch.continue2click_element(element2click)
    if cont =='clicked':
      ActionChains(webbrowser2focus).click(element2click).perform()
      time.sleep(2)
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    # fill in the contact formular
    element2click = Obj_ivd24immobilien_ch.check2click_element('//*[@class="form-control"]', 3)
    cont = Obj_ivd24immobilien_ch.continue2click_element(element2click)
    if cont == 'clicked':
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
    # fill in the form:
    try:
      xpath_submit = '//*[@id="reCaptchaForm"]/div[2]/div[6]/div[2]/button'
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[1]/div[2]/input', input_List['Firstname'])
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[1]/div[3]/input', input_List['Lastname'])
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[2]/div[1]/input', input_List['Email'])
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[2]/div[2]/input', input_List['Telephone'])
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[5]/div[1]/textarea ', input_List['Message'])
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[3]/div/input', input_List['Street']+' '+input_List['Housenumber'])
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[4]/div[1]/input', input_List['PostalCode'])
      Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[4]/div[2]/input', input_List['City'])
    except:
      try:
        xpath_submit = '//*[@id="reCaptchaForm"]/div[2]/div[4]/div[2]/button'
        Obj_ivd24immobilien_ch.fill_TextBox('//*[@id="reCaptchaForm"]/div[2]/div[3]/div[1]/textarea', input_List['Message'])
      except:
        print('\n-----> Complete the form manually to finish\n')
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n")
          if a != []:
            break
    # Submit the Form   
    element2click = Obj_ivd24immobilien_ch.check2click_element(xpath_submit, 3)
    cont = Obj_ivd24immobilien_ch.continue2click_element(element2click)
    if cont =='clicked':
      element2click.click()     ###################  Submitted ##################
      time.sleep(5)
      # if any error by sending:
      element2click = Obj_ivd24immobilien_ch.check2click_element(xpath_submit, 1, [None,None,'clickable'])
      while element2click != []:
        print("\n----->Finish filling the page and click send button!\n")
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n...")
          if a != []:
            break
        element2click = Obj_ivd24immobilien_ch.check2click_element(xpath_submit, 1, [None,None,'clickable'])
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
    webscrape.gather_log_info_ivd24immobilien(webbrowser2focus,_url2open[i], filepath)

    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")  
    
#webbrowser2focus.execute_script("window.history.go(-1)")

  return True  
#
#