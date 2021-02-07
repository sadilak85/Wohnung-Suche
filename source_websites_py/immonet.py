from driverinteraction import ImmobilienSuche
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
  filenamekeystr = 'immonet'
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded(webbrowser, filenamekeystr, 'angebot')
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

    # Scroll to contact formular and fill it: 
    ActionChains(webbrowser2focus).move_to_element(webbrowser2focus.find_element_by_xpath('//*[@id="sbc_submit"]')).perform()
    element2click = Obj_immonet_ch.check2click_element('//*[@id="sbc_salutation"]')
    cont = Obj_immonet_ch.continue2click_element(element2click)
    if cont =='clicked':
      ActionChains(webbrowser2focus).click(element2click).perform()
      #element2click.click()
      time.sleep(2)      
      pass
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue
    try:
      Select(element2click).select_by_visible_text(input_List['Salutation'])
    except:
      print('\n-----> Select manually the title: Herr/Frau\n')
      print("After finishing, press a key to continue\n")
      while True:
        a = input("\n-----> press any key to continue")
        if a != []:
          break
    try:
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_prename"]', input_List['Firstname'])
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_surname"]', input_List['Lastname'])
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_email"]', input_List['Email'])
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_phone"]', input_List['Telephone'])
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_annotations"]', input_List['Message'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      print("After finishing, press a key to continue\n")
      while True:
        a = input("\n-----> press any key to continue")
        if a != []:
          break
    # some extra information on some objects extra given
    try: 
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_contact_street"]', input_List['Street']+' '+input_List['Housenumber'])
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_contact_zip"]', input_List['PostalCode'])
      Obj_immonet_ch.fill_TextBox('//*[@id="sbc_contact_city"]', input_List['City'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      print("After finishing, press a key to continue\n")
      while True:
        a = input("\n-----> press any key to continue")
        if a != []:
          break
    #
    # submit the Form:  
    element2click = Obj_immonet_ch.check2click_element('//*[@id="sbc_submit"]')
    cont = Obj_immonet_ch.continue2click_element(element2click)
    if cont =='clicked':
      print(element2click)
      # element2click.click()   ###################  Burayi en son comment out yap !! ##################
      time.sleep(2)
      print('......................\n Message is successfully sent;)! \n......................')
    else:
      webbrowser2focus.close()
      time.sleep(2)      
      continue
  
    # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamekeystr+object_ID_list[i]+'.log')
    webscrape.gather_log_info_immonet(_url2open[i], filepath)

    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")   
  return True
#
#