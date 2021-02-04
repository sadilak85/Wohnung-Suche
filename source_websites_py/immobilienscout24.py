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


def _immobilienscout24(input_List):
  unformatted_url = 'https://www.immobilienscout24.de/Suche/de/{l}/wohnung-mieten?numberofrooms={r}.0-&price=-{p}.0&livingspace={q}.0-&pricetype=rentpermonth&sorting=2'
  url2open = unformatted_url.format(l=input_List['SearchLocation'], r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'])
  #
  Obj_immobilienscout24 = ImmobilienSuche(input_List)
  webbrowser = Obj_immobilienscout24.launchdriver(url2open)
  #
  # Captcha !!! get rid of this manually!
  while 'Robot' in webbrowser.title:
    print('waiting from user to get rid of Captcha manually to continue')
    time.sleep(15)
      
  Obj_immobilienscout24.scroll_down()
  #
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, 'Immobilienscout24_', 'expose')
  #
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
    cont = functions_sourcewebsite.cont_clicked_element (element2click)
    if cont =='clicked':
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue

    # Filling the form
    select_salutation = Obj_immobilienscout24_ch.check2click_element('//*[@id="contactForm-salutation"]')
    cont = functions_sourcewebsite.cont_clicked_element (select_salutation)
    if cont == 'clicked':
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)
      continue
    try:
      Select(select_salutation).select_by_visible_text('Herr')
    except Exception as err:
      print(err)
      print('Select manually the title: Herr/Frau')
      time.sleep(10)      
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
    # 
    # Submit Form 
    #
    time.sleep(3)
    element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[6]/div/button/span')
    cont = functions_sourcewebsite.cont_clicked_element (element2click)
    if cont =='error': #if no send button maybe check "weiter" button 
      element2click = Obj_immobilienscout24_ch.check2click_element('//*[@id="is24-expose-modal"]/div/div/div/div/div/div[1]/div[2]/div/div/div/form/div/div/div[5]/div/button/span')
      cont = functions_sourcewebsite.cont_clicked_element (element2click)
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
      print('Message is successfully sent;)!')
      # extract the page info into log file
      filepath = os.path.join(input_List['Outputdirectory'], 'Immobilienscout24_'+object_ID_list[i]+'.log')
      webscrape.gather_log_info_immobilienscout24(webbrowser2focus, filepath)
    #    
    webbrowser2focus.close()
  return True

