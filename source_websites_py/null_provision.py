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
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, filenamekeystr, 'angebot')
  #
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    if i == int(input_List['MaxObj2Search']):
      break
    _url2open[i] = _url2open[i].replace('https://www.null-provision.de/angebot/','https://www.immobilienscout24.de/expose/')
    Obj_null_provision_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_null_provision_ch.launchdriver(_url2open[i])
    #
    webbrowser2focus.execute_script("window.scrollTo(0, window.scrollY + 1500)")
    time.sleep(1)
    #
    element2click = Obj_null_provision_ch.check2click_element('//*[@id="is24-sticky-contact-area"]/div[1]/div/div[2]/a/span[1]')
    cont = Obj_null_provision_ch.cont_clicked_element (element2click)
    if cont =='clicked':
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue

    # Filling the form
    select_salutation = Obj_null_provision_ch.check2click_element('//*[@id="contactForm-salutation"]')
    cont = Obj_null_provision_ch.cont_clicked_element (select_salutation)
    if cont == 'clicked':
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
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-firstName"]', input_List['Firstname'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-lastName"]', input_List['Lastname'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-emailAddress"]', input_List['Email'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-phoneNumber"]', input_List['Telephone'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-street"]', input_List['Street'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-houseNumber"]', input_List['Housenumber'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-postcode"]', input_List['PostalCode'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-city"]', input_List['City'])
      Obj_null_provision_ch.fill_TextBox('//*[@id="contactForm-Message"]', input_List['Message'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      time.sleep(10)
    #
    # submit button ?
    #
    time.sleep(3)
    element2click = Obj_null_provision_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[6]/div/button/span')
    cont = Obj_null_provision_ch.cont_clicked_element (element2click)
    if cont =='error': #if no send button maybe check "weiter" button 
      element2click = Obj_null_provision_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[5]/div/button/span')
      cont = Obj_null_provision_ch.cont_clicked_element (element2click)
      if cont =='error':
        continue
      elif cont == 'continue':
        webbrowser2focus.close()
        time.sleep(2)      
        continue
      else: # last send button after manullay filling the last page after weiter button
        time.sleep('10')
        pass
    elif cont == 'continue':
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    else:
      print('..................\n Message is successfully sent;)! \n......................')
      # extract the page info into log file
      filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamekeystr+object_ID_list[i]+'.log')
      webscrape.gather_log_info_immobilienscout24(webbrowser2focus, filepath)
    # 
    webbrowser2focus.close()
  return True