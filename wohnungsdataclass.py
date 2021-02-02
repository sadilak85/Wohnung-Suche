from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
#
#from selenium.webdriver.firefox.options import Options
#
import time
#import pickle

class ImmobilienSuche:
  def __init__(self, input_List):
    self.browsertype = input_List['Browsertype']
    self.sourceweb = input_List['Sourceweb']
    self.firstname = input_List['Firstname']
    self.lastname = input_List['Lastname']
    self.email = input_List['Email']
    self.message = input_List['Message']
    self.SearchLocation = input_List['SearchLocation']
    self.Budget = input_List['Budget']
    self.TotalRooms = input_List['TotalRooms']
    self.SurfaceArea = input_List['SurfaceArea']
    self.cookiesfilename = "Cookies/Cookiesfor_{a}_{b}.pkl".format(a=self.browsertype, b=self.sourceweb)
    self.chromeprofilepath = input_List['ChromeUserProfilePath']
    self.driver = []    # creates a webdriver
    self.element = []   # elements in html

  def launchdriver(self, _url2open):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-data-dir='+self.chromeprofilepath)
    chrome_options.add_argument("start-maximized")
    #chrome_options.add_argument("window-size=1200x600")

    try:
      if self.browsertype =='Ie':
        self.driver = webdriver.Ie(executable_path=r'./drivers/IEDriverServer.exe')
      if self.browsertype =='Chrome':
        self.driver = webdriver.Chrome(executable_path=r'./drivers/chromedriver.exe', chrome_options=chrome_options)
      if self.browsertype =='Firefox':
        self.driver = webdriver.Firefox(executable_path=r'./drivers/geckodriver.exe')
    except:
      print('\n\nYou must close all opened selenium browser drivers then restart the process again!\n')
      quit()

    #self.driver.maximize_window()
    self.driver.get(_url2open)
    return self.driver

  #def load_cookies(self):
  #  pickle.dump(self.driver.get_cookies() , open(self.cookiesfilename,"wb"))

  #def save_cookies(self):
  #  cookies = pickle.load(open(self.cookiesfilename, "rb"))
  #  for cookie in cookies:
  #    self.driver.add_cookie(cookie)

  def scroll_down(self):
    lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
      lastCount = lenOfPage
      time.sleep(3)
      lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
      if lastCount==lenOfPage:
        match=True

  def check2click_element (self, _pathstring):
    try:
      self.element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, _pathstring)))
      print('visibility of element located achieved')
      return self.element
    except TimeoutException:
      print ("Loading took too much time for visibility of element located!")
      self.element =[]
    try:
      self.element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, _pathstring)))
      print('presence of element located achieved')
      return self.element
    except TimeoutException:
      print ("Loading took too much time for presence of element located!")
      self.element =[]
    try:         
      self.element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, _pathstring)))
      print('presence of element to be clickable achieved')
      return self.element
    except TimeoutException:
      print ("Loading took too much time for element clickable!")
      self.element =[]        
    return self.element

  def fill_TextBox(self, _pathstring, _str):
    textbox = self.driver.find_element_by_xpath(_pathstring)
    textbox.clear()
    textbox.send_keys(_str)

#
#
#