import time
import os

def get_objectID(objecturl, _keystr):
  try:
    object_ID = objecturl.split(_keystr+'/')[1].split('?')[0]
  except:
    object_ID = None
  return object_ID

def search_files_w_Object_ID(_checkfilenamestr):
  check = False
  for dirpath, dirnames, filenames in os.walk("Output"):
    for filename in [f for f in filenames if _checkfilenamestr in f]:
      check = True
  return check

def wait_objects_loaded(_driver, _urlnamestr, _keystr):
  _url2open = []
  object_ID_list = []
  while object_ID_list == []:
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
    time.sleep(5)
  return _url2open, object_ID_list
  
def cont_clicked_element(_element2click):
  if _element2click != []:
    try:
      _element2click.click()
      time.sleep(2)
      return 'clicked'
    except:
      print("Button for 'Contact' can not be clicked, it is being obscured by something, the process is aborting...")
      return 'error'   
  else:
    print("Button for 'Contact' does not exist, skipping this task...")
    return 'continue' 