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

def _immonet(input_List):
  unformatted_url = 'https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&listsize=26&objecttype=1&locationname={l}&acid=&actype=&city={i}&ajaxIsRadiusActive=true&sortby=0&suchart=2&radius=0&pcatmtypes=1_2&pCatMTypeStoragefield=1_2&parentcat=1&marketingtype=2&fromprice=&toprice={p}&fromarea={q}&toarea=&fromplotarea=&toplotarea=&fromrooms={r}&torooms=&objectcat=-1&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen'
  url2open = unformatted_url.format(l=input_List['SearchLocation'].split('/')[1], r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'],
                                    i='121673' if input_List['SearchLocation'] == 'bayern/muenchen'
                                    else '87372' if input_List['SearchLocation'] == 'berlin/berlin'
                                    else '109447' if input_List['SearchLocation'] == 'hamburg/hamburg'
                                    else '113144' if input_List['SearchLocation'] == 'nordrhein-westfalen/koeln'
                                    else '105043' if input_List['SearchLocation'] == 'hessen/frankfurt-am-main'
                                    else '143262' if input_List['SearchLocation'] == 'baden-wuerttemberg/stuttgart'
                                    else '100207' if input_List['SearchLocation'] == 'nordrhein-westfalen/duesseldorf'
                                    else '121673')
  #
  Obj_immonet = ImmobilienSuche(input_List)
  webbrowser = Obj_immonet.launchdriver(url2open)
  #
  filenamestr = 'immonet'
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, filenamestr, 'angebot')
  #Obj_immonet.save_cookies()
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    if i == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    Obj_immonet_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_immonet_ch.launchdriver(_url2open[i])

    # Click on the "Contact to" button
    webbrowser2focus.execute_script("window.scrollTo(0, window.scrollY + 1500)")
    time.sleep(2)

    element2click = Obj_immonet_ch.check2click_element('//*[@id="is24-sticky-contact-area"]/div[1]/div/div[2]/a/span[1]')
    cont = Obj_immonet_ch.cont_clicked_element (element2click)
    if cont =='error':
      return False
    elif cont == 'continue':
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    else:
      pass

    # Filling the form
    select_salutation = Obj_immonet_ch.check2click_element('//*[@id="contactForm-salutation"]')
    cont = Obj_immonet_ch.cont_clicked_element (select_salutation)
    if cont =='error':
      return False
    elif cont == 'continue':
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    else:
      pass
    try:
      Select(select_salutation).select_by_visible_text(input_List['Salutation'])
    except:
      print('\n-----> Select manually the title: Herr/Frau\n')
      time.sleep(10)
      pass
    try:
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-firstName"]', input_List['Firstname'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-lastName"]', input_List['Lastname'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-emailAddress"]', input_List['Email'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-phoneNumber"]', input_List['Telephone'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-street"]', input_List['Street'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-houseNumber"]', input_List['Housenumber'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-postcode"]', input_List['PostalCode'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-city"]', input_List['City'])
      Obj_immonet_ch.fill_TextBox('//*[@id="contactForm-Message"]', input_List['Message'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      time.sleep(10)


    # submit button ?  wait to be submittable

    # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamestr+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immonet(webbrowser2focus, filepath)
    
    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")         
  return True