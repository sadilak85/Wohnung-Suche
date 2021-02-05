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

def _immonet(input_List):
  unformatted_url = 'https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&listsize=26&objecttype=1&locationname={l}&acid=&actype=&city={i}&ajaxIsRadiusActive=true&sortby=0&suchart=2&radius=0&pcatmtypes=1_2&pCatMTypeStoragefield=1_2&parentcat=1&marketingtype=2&fromprice=&toprice={p}&fromarea={q}&toarea=&fromplotarea=&toplotarea=&fromrooms={r}&torooms=&objectcat=-1&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen'
  url2open = unformatted_url.format(l=input_List['SearchLocation'].split('/')[1], r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'],
                                    i='121673' if input_List['SearchLocation'] == 'bayern/muenchen'
                                    else '121673' if input_List['SearchLocation'] == 'berlin/berlin'
                                    else '121673' if input_List['SearchLocation'] == 'hamburg/hamburg'
                                    else '121673' if input_List['SearchLocation'] == 'nordrhein-westfalen/koeln'
                                    else '121673' if input_List['SearchLocation'] == 'hessen/frankfurt-am-main'
                                    else '121673' if input_List['SearchLocation'] == 'baden-wuerttemberg/stuttgart'
                                    else '121673' if input_List['SearchLocation'] == 'nordrhein-westfalen/duesseldorf')
  #
  Obj_null_provision = ImmobilienSuche(input_List)
  webbrowser = Obj_null_provision.launchdriver(url2open)
  #
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, 'null_provision_', 'angebot')
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
    cont = functions_sourcewebsite.cont_clicked_element (element2click)
    if cont =='error':
      return False
    elif cont == 'continue':
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    else:
      pass

    # Filling the form
    select_salutation = Obj_null_provision_ch.check2click_element('//*[@id="contactForm-salutation"]')
    cont = functions_sourcewebsite.cont_clicked_element (select_salutation)
    if cont =='error':
      return False
    elif cont == 'continue':
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    else:
      pass
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
    filepath = os.path.join(input_List['Outputdirectory'], 'null_provision_'+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immobilienscout24(webbrowser2focus, filepath)
    
    webbrowser2focus.close()
  return True