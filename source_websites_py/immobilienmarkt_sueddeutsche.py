from wohnungsdataclass import ImmobilienSuche
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
  # Open the objects found after search

  xpath = "//div[contains(@class, 'hitHeadline')]"

  element2click_list = webbrowser.find_elements_by_xpath(xpath)
  max_elts = len(element2click_list)

  for i in range(max_elts-1):
    if i == int(input_List['MaxObj2Search']):
      break
    element2click_list = webbrowser.find_elements_by_xpath(xpath)
    try:
      if element2click_list[i].is_displayed():
        element2click_list[i].click()
        Obj_sueddeutsche.scroll_down()
        object_ID = webbrowser.find_element_by_class_name('exposeId').find_element_by_xpath('.//span').get_attribute('textContent')
        _filenamestr = 'Info_Immobilienmarkt_sueddeutsche_'+object_ID
        if not functions_sourcewebsite.search_files_w_Object_ID(_filenamestr):
          # extract the page info into log file
          filepath = os.path.join(input_List['Outputdirectory'], _filenamestr+'.log')
          webscrape.gather_log_info_immobilienmarkt_sueddeutsche('http://immo.sz.de/'+object_ID, filepath)        
          # fill in the contact formular
          try:
            Obj_sueddeutsche.fill_TextBox('//*[@id="idDRfirstname"]', input_List['Firstname'])
            Obj_sueddeutsche.fill_TextBox('//*[@id="idDRlastname"]', input_List['Lastname'])
            Obj_sueddeutsche.fill_TextBox('//*[@id="idDRfrom"]', input_List['Email'])
            Obj_sueddeutsche.fill_TextBox('//*[@id="idDRphone"]', input_List['Telephone'])
            Obj_sueddeutsche.fill_TextBox('//*[@id="idDRSenderZusatz"]', input_List['Message'])
          except:
            print('\n-----> Complete the form manually to finish\n')
            time.sleep(10)
          #click radio buttons
          try:
            webbrowser.find_element_by_xpath('//*[@id="idDRSenderInfo"]').click()
            webbrowser.find_element_by_xpath('//*[@id="idDRSenderTermin"]').click()
            webbrowser.find_element_by_xpath('//*[@id="idDRSenderCall"]').click()
          except:
            print("\n-----> click the check boxes in the form manually!\n")
            time.sleep(10)
            pass
          # click on submit button
          submitbutton = webbrowser.find_element_by_xpath('//*[@id="directReqShort"]')
          #submitbutton.click()
          print(submitbutton)
  
        webbrowser.execute_script("window.history.go(-1)")
    except:
      pass

  #Obj_sueddeutsche_ch.save_cookies()
  webbrowser.close()
  return True  