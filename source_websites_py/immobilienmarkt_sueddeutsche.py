from driverinteraction import ImmobilienSuche
import functions_sourcewebsite
import webscrape
#
import time
import os
import os.path
#
#
#import pdb
#pdb.set_trace()
#

def _immobilienmarkt_sueddeutsche(input_List):
  unformatted_url = 'https://immobilienmarkt.sueddeutsche.de/index.php?action=immo/suchen/trliste/home#&atype=a&pTo={p}&aFrom={q}&rFrom={r}&reg={l}&offset=0&sort=-time'
  url2open = unformatted_url.format(  l = 'DEU091620000001' if input_List['SearchLocation'] == 'bayern/muenchen' 
                                          else 'DEU120000000001' if input_List['SearchLocation'] == 'berlin/berlin' 
                                          else 'DEU020000000001' if input_List['SearchLocation'] == 'hamburg/hamburg'
                                          else 'DEU053150000001' if input_List['SearchLocation'] == 'nordrhein-westfalen/koeln'
                                          else 'DEU060000000001' if input_List['SearchLocation'] == 'hessen/frankfurt-am-main'
                                          else 'DEU081110000001' if input_List['SearchLocation'] == 'baden-wuerttemberg/stuttgart'
                                          else 'DEU064120000001' if input_List['SearchLocation'] == 'nordrhein-westfalen/duesseldorf'
                                          else 'DEU091620000001', r=input_List['TotalRooms'], p=input_List['Budget'], q=input_List['SurfaceArea'])

  Obj_sueddeutsche = ImmobilienSuche(input_List)
  webbrowser = Obj_sueddeutsche.launchdriver(url2open)
  #
  filenamekeystr = 'Immobilienmarkt_sueddeutsche_'
  _url2open, object_ID_list = functions_sourcewebsite.wait_objects_loaded_sueddeutsche(webbrowser, filenamekeystr)
  #
  webbrowser.close()
  #
  # Open the objects found after search
  for i in range(len(_url2open)):
    if i == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    Obj_sueddeutsche_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_sueddeutsche_ch.launchdriver(_url2open[i])
    #
    try:
      webbrowser2focus.execute_script("arguments[0].scrollIntoView();", webbrowser2focus.find_element_by_xpath('//*[@id="directReqShort"]'))
    except:
      Obj_sueddeutsche_ch.scroll_down()
    # fill in the contact formular
    try:
      Obj_sueddeutsche_ch.fill_TextBox('//*[@id="idDRfirstname"]', input_List['Firstname'])
      Obj_sueddeutsche_ch.fill_TextBox('//*[@id="idDRlastname"]', input_List['Lastname'])
      Obj_sueddeutsche_ch.fill_TextBox('//*[@id="idDRfrom"]', input_List['Email'])
      Obj_sueddeutsche_ch.fill_TextBox('//*[@id="idDRphone"]', input_List['Telephone'])
      Obj_sueddeutsche_ch.fill_TextBox('//*[@id="idDRSenderZusatz"]', input_List['Message'])
    except:
      print('\n-----> Complete the form manually to finish\n')
      time.sleep(10)
    #click radio buttons
    try:
      webbrowser2focus.find_element_by_xpath('//*[@id="idDRSenderInfo"]').click()
      webbrowser2focus.find_element_by_xpath('//*[@id="idDRSenderTermin"]').click()
      webbrowser2focus.find_element_by_xpath('//*[@id="idDRSenderCall"]').click()
    except:
      print("\n-----> click the check boxes in the form manually!\n")
      time.sleep(10)
    # Submit the Form
    element2click = Obj_sueddeutsche_ch.check2click_element('//*[@id="directReqShort"]')
    cont = Obj_sueddeutsche_ch.continue2click_element(element2click)
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
    webscrape.gather_log_info_immobilienmarkt_sueddeutsche(_url2open[i], filepath)

    webbrowser2focus.close()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")  
    
#webbrowser2focus.execute_script("window.history.go(-1)")

  return True  