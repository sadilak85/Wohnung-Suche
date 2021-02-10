import time
import os
#

def get_objectID(objecturl, _keystr):
  try:
    object_ID = objecturl.split(_keystr)[-1].split('?')[0]
  except:
    object_ID = ''  
  return object_ID.lstrip('/')

def search_files_w_Object_ID(_checkfilenamestr):
  check = False
  for dirpath, dirnames, filenames in os.walk("Output"):
    for filename in [f for f in filenames if _checkfilenamestr in f]:
      check = True
  return check

def extract_object_url_ID(_driver, _urlnamestr, _keystr):
  _url2open = []
  object_ID_list = []
  time.sleep(2)
  for link in _driver.find_elements_by_tag_name('a'):
    objecturl = link.get_attribute("href")
    if objecturl != None:
      if _keystr in objecturl:
        object_ID = get_objectID(objecturl, _keystr)
        check = search_files_w_Object_ID(_urlnamestr+object_ID)
        if not check:
          if objecturl not in _url2open:
            _url2open.append(objecturl)
          if object_ID not in object_ID_list:
            object_ID_list.append(object_ID)
  return _url2open, object_ID_list

def extract_object_url_ID_sueddeutsche(_driver, _urlnamestr):
  _url2open = []
  object_ID_list = []
  time.sleep(2)
  _keystr = '/'
  for link in _driver.find_elements_by_xpath("//div[@class='hitHeadline']/a"):
    objecturl = link.get_attribute("href")
    if objecturl != None:
      if _keystr in objecturl:
        object_ID = get_objectID(objecturl, _keystr)
        check = search_files_w_Object_ID(_urlnamestr+object_ID)
        if not check:
          if objecturl not in _url2open:
            _url2open.append(objecturl)
          if object_ID not in object_ID_list:
            object_ID_list.append(object_ID)
  return _url2open, object_ID_list

def extract_object_url_ID_ivd24immobilien(_driver, _urlnamestr):
  _url2open = []
  object_ID_list = []
  time.sleep(2)
  _keystr = '-'
  for link in _driver.find_elements_by_xpath("//p[@class='expose-button float-right']/a"):
    objecturl = link.get_attribute("href")
    if objecturl != None:
      if _keystr in objecturl:
        object_ID = get_objectID(objecturl, _keystr)
        check = search_files_w_Object_ID(_urlnamestr+object_ID)
        if not check:
          if objecturl not in _url2open:
            _url2open.append(objecturl)
          if object_ID not in object_ID_list:
            object_ID_list.append(object_ID)
  return _url2open, object_ID_list

#
#
#