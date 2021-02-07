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
def _immobilienscout24(input_List):
  unformatted_url = 'https://www.immobilienscout24.de/Suche/de/{l}/wohnung-mieten?numberofrooms={r}.0-&price=-{p}.0&livingspace={q}.0-&pricetype=rentpermonth&sorting=2'
  url2open = unformatted_url.format(l=input_List['SearchLocation'], r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'])
  #
  Obj_immobilienscout24 = ImmobilienSuche(input_List)
  webbrowser = Obj_immobilienscout24.launchdriver(url2open)
  #
  Obj_immobilienscout24.scroll_down()
  #
  filenamekeystr = 'Immobilienscout24_'
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, filenamekeystr, 'expose')
  #
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    if i == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    Obj_immobilienscout24_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_immobilienscout24_ch.launchdriver(_url2open[i])
    #
    webbrowser2focus.execute_script("window.scrollTo(0, window.scrollY + 1500)")
    time.sleep(2)
    #
    element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-sticky-contact-area"]/div[1]/div/div[2]/a/span[1]')
    cont = Obj_immobilienscout24_ch.continue2click_element(element2click)
    if cont =='clicked':
      element2click.click()
      time.sleep(2)      
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue

    # Filling the form
    element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="contactForm-salutation"]')
    cont = Obj_immobilienscout24_ch.continue2click_element(element2click)
    if cont == 'clicked':
      element2click.click()
      time.sleep(2)      
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)
      continue
    try:
      Select(element2click).select_by_visible_text(input_List['Salutation'])
    except:
      print("----->\nSelect manually the title: Herr/Frau")
      print("\nAfter finishing, press a key to continue\n")
      while True:
        a = input("\n-----> press any key to continue")
        if a != []:
          break
    try:
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-Message"]', input_List['Message'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-firstName"]', input_List['Firstname'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-lastName"]', input_List['Lastname'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-emailAddress"]', input_List['Email'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-phoneNumber"]', input_List['Telephone'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      print("\nAfter finishing, press a key to continue\n")
      while True:
        a = input("\n-----> press any key to continue")
        if a != []:
          break      
    # some extra information on some objects extra given
    try: 
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-street"]', input_List['Street'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-houseNumber"]', input_List['Housenumber'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-postcode"]', input_List['PostalCode'])
      Obj_immobilienscout24_ch.fill_TextBox('//*[@id="contactForm-city"]', input_List['City'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      print("\nAfter finishing, press a key to continue\n")
      while True:
        a = input("\n-----> press any key to continue")
        if a != []:
          break
    # 
    # Submit Form 
    #
    time.sleep(1)
    # Check if "Anfrage Senden" button exists:
    element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[6]/div/button/span')
    cont = Obj_immobilienscout24_ch.continue2click_element(element2click)
    if cont =='obscured':  
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    elif cont == 'ignore': #if no send button maybe check "Weiter" button
      print("trying to click on 'Weiter' button")
      # Check if "Weiter" button exists:
      element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[5]/div/button/span')
      cont = Obj_immobilienscout24_ch.continue2click_element(element2click)
      if cont =='obscured':
        continue
      elif cont == 'ignore':
        webbrowser2focus.close()
        time.sleep(2)
        continue
      else: # last page "Anfrage Senden" button, after manullay filling this page with extra optional questions
        element2click.click()
        time.sleep(4)
        element2click = webbrowser2focus.find_elements_by_xpath('//*[@id="is24-expose-modal"]/div/div/div/div/div[1]/div/div/div/form/div[5]/button')
        while element2click != []:
          print("\n----->Finish filling this optional page and click 'Anfrage Senden' button!\n")
          print("\nAfter finishing, press a key to continue\n")
          while True:
            a = input("\n-----> press any key to continue")
            if a != []:
              break
          element2click = webbrowser2focus.find_elements_by_xpath('//*[@id="is24-expose-modal"]/div/div/div/div/div[1]/div/div/div/form/div[5]/button')
    else:
    #  element2click.click()  ###################  Burayi en son comment out yap !! ##################
      time.sleep(2)

    print('......................\n Message is successfully sent;)! \n......................')
    # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamekeystr+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immobilienscout24(webbrowser2focus, filepath)
    #    
    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")   
  return True

