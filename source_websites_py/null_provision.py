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
  filenamekeystr = 'null_provision_'
  _url2open, object_ID_list = functions_sourcewebsite.extract_object_url_ID(webbrowser, filenamekeystr, 'angebot')
  #
  webbrowser.close()
  #
  totalobj2process = 0
  # Open the objects found after search
  for i in range(len(_url2open)):
    if totalobj2process == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    _url2open[i] = _url2open[i].replace('https://www.null-provision.de/angebot/','https://www.immobilienscout24.de/expose/')
    Obj_null_provision_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_null_provision_ch.launchdriver(_url2open[i])
    #
    webbrowser2focus.execute_script("window.scrollTo(0, window.scrollY + 1500)")
    time.sleep(1)
    #
    element2click = Obj_null_provision_ch.check2click_element('//*[@id="is24-sticky-contact-area"]/div[1]/div/div[2]/a/span[1]', 3)
    cont = Obj_null_provision_ch.continue2click_element(element2click)
    if cont =='clicked':
      element2click.click()
      time.sleep(2)
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue

    # Filling the form
    element2click = Obj_null_provision_ch.check2click_element('//*[@id="contactForm-salutation"]', 3)
    cont = Obj_null_provision_ch.continue2click_element(element2click)
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
        a = input("\n-----> Press Enter to continue\n...")
        if a != []:
          break
    try:
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-Message"]', input_List['Message'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-firstName"]', input_List['Firstname'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-lastName"]', input_List['Lastname'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-emailAddress"]', input_List['Email'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-phoneNumber"]', input_List['Telephone'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      print("\nAfter finishing, press a key to continue\n")
      while True:
        a = input("\n-----> Press Enter to continue\n")
        if a != []:
          break
    # some extra information on some objects extra given
    try: 
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-street"]', input_List['Street'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-houseNumber"]', input_List['Housenumber'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-postcode"]', input_List['PostalCode'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-city"]', input_List['City'])
    except:
      pass
    # 
    # Submit Form 
    #
    time.sleep(1)
    # Check if "Anfrage Senden" button exists:
    element2click = Obj_null_provision_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[6]/div/button/span', 3)
    cont = Obj_null_provision_ch.continue2click_element(element2click)
    if cont =='obscured':  
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    elif cont == 'ignore': #if no send button maybe check "Weiter" button
      print("trying to click on 'Weiter' button")
      # Check if "Weiter" button exists:
      element2click = Obj_null_provision_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[5]/div/button/span', 3)
      cont = Obj_null_provision_ch.continue2click_element(element2click)
      if cont =='obscured':
        continue
      elif cont == 'ignore':
        webbrowser2focus.close()
        time.sleep(2)
        continue
      else: # last page with "Anfrage Senden" button, after manullay filling this page with extra optional questions, then continue..
        element2click.click()
        time.sleep(4)
        element2click = webbrowser2focus.find_elements_by_xpath('//*[@id="is24-expose-modal"]/div/div/div/div/div[1]/div/div/div/form/div[5]/button')
        while element2click != []:
          print("\n----->Finish filling this optional page and click 'Anfrage Senden' button!\n")
          print("\nAfter finishing, press a key to continue\n")
          while True:
            a = input("\n-----> Press Enter to continue\n")
            if a != []:
              break
          element2click = webbrowser2focus.find_elements_by_xpath('//*[@id="is24-expose-modal"]/div/div/div/div/div[1]/div/div/div/form/div[5]/button')
          if  element2click == []: # submitted manually
            print("\nSubmitted manually and will save a log file as usual\n")
            pass
    else:
      element2click.click()     ###################  Submitted ##################
      time.sleep(2)

    print('......................\n Message is successfully sent;)! \n......................')
    totalobj2process = totalobj2process + 1
    # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamekeystr+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immobilienscout24(webbrowser2focus,_url2open[i], filepath)
    #    
    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")   
  return True
#
#
#