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
def _wohnungsboerse(input_List):
  _loc = input_List['SearchLocation'].split('/')[1]
  unformatted_url = 'https://www.wohnungsboerse.net/searches/index/marketing_type:miete/object_type:1/city:{l}/country:de/maxprice:{p}/minrooms:{r}/minsize:{q}/state:2'
  url2open = unformatted_url.format(l=_loc.split('-')[0] if '-' in _loc else _loc, 
                                    r = '2' if int(input_List['TotalRooms']) < 3
                                    else '3' if int(input_List['TotalRooms']) < 4
                                    else '4' if int(input_List['TotalRooms']) < 5
                                    else '5' if int(input_List['TotalRooms']) < 6
                                    else '6' if int(input_List['TotalRooms']) < 7
                                    else '7' if int(input_List['TotalRooms']) < 8
                                    else '8' ,                                    
                                    p= '400' if int(input_List['Budget']) <= 400
                                    else '500' if int(input_List['Budget']) <= 500
                                    else '700' if int(input_List['Budget']) <= 700
                                    else '1000' if int(input_List['Budget']) <= 1000
                                    else '1200' if int(input_List['Budget']) <= 1200
                                    else '1500' if int(input_List['Budget']) <= 1500
                                    else '2000' , 
                                    q='30' if int(input_List['SurfaceArea']) < 40
                                    else '40' if int(input_List['SurfaceArea']) < 50
                                    else '50' if int(input_List['SurfaceArea']) < 60
                                    else '60' if int(input_List['SurfaceArea']) < 80
                                    else '80' if int(input_List['SurfaceArea']) < 100
                                    else '100' if int(input_List['SurfaceArea']) < 120
                                    else '120' )
  #
  Obj_wohnungsboerse = ImmobilienSuche(input_List)
  webbrowser = Obj_wohnungsboerse.launchdriver(url2open)
  #
  #
  filenamekeystr = 'wohnungsboerse_'
  _url2open, object_ID_list = functions_sourcewebsite.extract_object_url_ID(webbrowser, filenamekeystr,'https://www.wohnungsboerse.net/immodetail/')
  
  while _url2open == []:
    print("\nGet rid of the Captcha first!\n")
    while True:
      a = input("\n-----> Press Enter to continue\n")
      if a != []:
        break
    _url2open, object_ID_list = functions_sourcewebsite.extract_object_url_ID(webbrowser, filenamekeystr,'https://www.wohnungsboerse.net/immodetail/')

  webbrowser.close()
  #
  totalobj2process = 0
  # Open the objects found after search
  for i in range(len(_url2open)):
    if totalobj2process == int(input_List['MaxObj2Search']):
      print('max number of objects to search is achieved')
      break
    Obj_wohnungsboerse_ch = ImmobilienSuche(input_List)
    webbrowser2focus = Obj_wohnungsboerse_ch.launchdriver(_url2open[i])
    try:
      print(webbrowser2focus.title)
      logfilestr = '\n'
      logfilestr = logfilestr + webbrowser2focus.find_element_by_xpath('/html/body/div[6]/div[8]/div[10]/div[1]').text + '\n'
      logfilestr = logfilestr + webbrowser2focus.find_element_by_xpath('/html/body/div[6]/div[8]/div[10]/div[5]').text + '\n'
      logfilestr = logfilestr + webbrowser2focus.find_element_by_xpath('/html/body/div[6]/div[8]/div[11]/div[1]').text + '\n'
      logfilestr = logfilestr + webbrowser2focus.find_element_by_xpath('/html/body/div[6]/div[8]/div[13]/div[1]/div[4]').text + '\n'
    except:
      print("\nsome information could not be written to log file\n")
    #
    # Click on the "Contact to" button 
    #
    try:
      tmp = webbrowser2focus.find_element_by_xpath('//img[@alt="Immowelt"]') # check if powered by immowelt
    except:
      tmp = None
    if tmp == None:
      xpath_ = "//*[contains(text(), 'Anbieter kontaktieren')]"  #'/html/body/div[6]/div[8]/div[10]/div[2]/a'
      checkimmowelt = False
    else:
      xpath_ = "//*[contains(text(), 'Anbieter kontaktieren')]" # powered by immowelt
      checkimmowelt = True
    ActionChains(webbrowser2focus).move_to_element(webbrowser2focus.find_element_by_xpath(xpath_)).perform()
    element2click = Obj_wohnungsboerse_ch.check2click_element(xpath_, 3)
    cont = Obj_wohnungsboerse_ch.continue2click_element(element2click)
    if cont =='clicked':
      ActionChains(webbrowser2focus).click(element2click).perform()
      time.sleep(2)
    else:
      print('\nsomething went wrong for this object!\n')
      webbrowser2focus.quit()
      time.sleep(2)      
      continue
    #
    # Filling the FORM
    #
    if checkimmowelt == True:
      webbrowser2focus.switch_to.window(webbrowser2focus.window_handles[1])
      element2click = Obj_wohnungsboerse_ch.check2click_element('//*[@id="salutation"]', 3)
      cont = Obj_wohnungsboerse_ch.continue2click_element(element2click)
      if cont =='clicked':
        element2click.click()
        time.sleep(2) 
      else:
        webbrowser2focus.quit()
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
      try:
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="firstname"]', input_List['Firstname'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="lastname"]', input_List['Lastname'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="email"]', input_List['Email'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="tel"]', input_List['Telephone'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="message"]', input_List['Message'])
      except:
        print('\n-----> Complete the form manually to finish\n')
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n")
          if a != []:
            break
      try:
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="street"]', input_List['Street']+' '+input_List['Housenumber'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="zipcode"]', input_List['PostalCode'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="city"]', input_List['City'])
      except:
        pass
      # Click on the radioboxes under message box
      try:
        element2click = Obj_wohnungsboerse_ch.check2click_element('//*[@id="requestMoreInformation"]', 3)
        Obj_wohnungsboerse_ch.continue2click_element(element2click)
        element2click.click()
        time.sleep(2)
        element2click = Obj_wohnungsboerse_ch.check2click_element('//*[@id="requestCallback"]', 3)
        Obj_wohnungsboerse_ch.continue2click_element(element2click)
        element2click.click()
        time.sleep(2)
      except:
        print("\n-----> click the check boxes: 'Infomaterial anfordern' 'Rückruf'\n")
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n")
          if a != []:
            break
      _submit_btn_xpath = '//*[@id="btnContactSend"]'
      _next_btn_xpath = '//*[@id="btnStepForward"]'
    else:
      try:
        logfilestr = logfilestr +'\n'+webbrowser2focus.find_element_by_xpath('//*[@id="contact-form"]/div/div[1]').text
      except:
        pass  
      try:
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="name-ctrl"]', input_List['Firstname']+' '+input_List['Lastname'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="email-ctrl"]', input_List['Email'])
        Obj_wohnungsboerse_ch.fill_TextBox('//*[@id="msg-ctrl"]', input_List['Message'])
      except:
        print('\n-----> Complete the form manually to finish\n')
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n")
          if a != []:
            break
      # Click on the radioboxes under message box
      try:
        element2click = Obj_wohnungsboerse_ch.check2click_element('//*[@id="datenschutz"]', 3)
        Obj_wohnungsboerse_ch.continue2click_element(element2click)
        element2click.click()
        time.sleep(2)
       # element2click = Obj_wohnungsboerse_ch.check2click_element('//*[@id="recaptcha-anchor"]/div[1]', 3)
       # Obj_wohnungsboerse_ch.continue2click_element(element2click)
       # element2click.click()
       # time.sleep(2)
      except:
        print('\n-----> Complete the form manually to finish\n')
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n")
          if a != []:
            break 
      _submit_btn_xpath = '//*[@id="contact-form-submit"]'
      _next_btn_xpath = ''
    #
    # Submit the Form 
    #
    element2click = Obj_wohnungsboerse_ch.check2click_element(_submit_btn_xpath, 1, ['visible',None,None])
    element2click2 = Obj_wohnungsboerse_ch.check2click_element(_next_btn_xpath, 1, ['visible',None,None])
    cont = Obj_wohnungsboerse_ch.continue2click_element(element2click)
    cont2 = Obj_wohnungsboerse_ch.continue2click_element(element2click2)
    if cont =='clicked' or cont2 =='clicked':
      if cont2 =='clicked':
        element2click2.click() # Weiter Button click
      else:
        # element2click.click()   ###################  Burayi en son comment out yap !! ##################
        time.sleep(5)
      # if any error by sending + After weiter button there is extra form manually to fill:
      element2click = Obj_wohnungsboerse_ch.check2click_element(_submit_btn_xpath, 1, [None,None,'clickable'])
      while element2click != []:
        print("\n----->Finish filling the page and click send button!\n")
        print("\nAfter finishing, press a key to continue\n")
        while True:
          a = input("\n-----> Press Enter to continue\n...")
          if a != []:
            break
        element2click = Obj_wohnungsboerse_ch.check2click_element(_submit_btn_xpath, 1, [None,None,'clickable'])
        if  element2click == []: # submitted manually
          print("\nSubmitted manually and will save a log file as usual\n")
          pass
      print('......................\n Message is successfully sent;)! \n......................')
      totalobj2process = totalobj2process + 1
    else:
      webbrowser2focus.quit()
      time.sleep(2)      
      continue
    # extract the page info into log file
    filepath = os.path.join(input_List['Outputdirectory'], 'Info_'+filenamekeystr+object_ID_list[i]+'.log')
    with open(filepath, mode='w') as outfile:
      outfile.write("\nWebsource: "+_url2open[i]+"\n")
      outfile.write(logfilestr)

    webbrowser2focus.quit()
  if _url2open == []:
    print("\nOops! You did a very unique thing!")
    print("\nAll objects found are already processed in a previous session.")
    print("\nIf you want to process on some of those objects again, you must delete their log files in 'Output' folder!!!")
    print("\n-----------------------------------------------------------")   
  return True
#
#