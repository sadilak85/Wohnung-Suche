import smtplib
from email.message import EmailMessage
from string import Template
import os.path
from os import walk
from pathlib import Path 
import re

import pdb
#pdb.set_trace()

 
def searchEmails(_outdirsession):
  _outfile = Path(_outdirsession) / 'ExtractedEmails'
  if not os.path.exists(_outfile):
    os.mkdir(_outfile)
  _, _, filenames = next(walk(_outdirsession))
  for filename in filenames:
    filepath = Path(_outdirsession) / filename
    _check = False
    with open(filepath, mode='r', encoding='unicode_escape') as f:
      _url = f.readline() # first line is for url
      _title = f.readline() # second line is for title 
      _info = [_url.strip(), _title]
      for line in f:
        for word in line.split():
          if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", word):
            _info.append(word)
            _check = True
      if _check == True:
        filenamestr = "ExtractedEmails_"+filename
        open(Path(_outfile/filenamestr), 'w').close()
        with open(Path(_outfile/filenamestr), mode='a', encoding="utf-8") as f:
          f.write("\n")
          for i in _info:
            f.write("%s\n" % i)
  return True

def getInfofromFile(_outdirsession):
  _infile = Path(_outdirsession) / "ExtractedEmails"
  _, _, filenames = next(walk(_infile))
  info_dict = {"emails":[],"titles":[],"urls":[]}
  for filename in filenames:
    filepath = Path(_infile) / filename
    _email = []
    _url = ''
    _title = ''
    with open(filepath, mode='r', encoding="utf-8") as f:
      _index = 0
      _tmpindex = 0
      while True:
        _tmp = f.readline()
        _index = _index+1
        if _tmp == '':
          break
        else:
          if _tmp.strip() == '':
            continue
          else:
            if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", _tmp):
              if _tmp.strip() not in _email:
                _email.append(_tmp.strip())
            elif 'http' in _tmp:
              _url = _tmp.strip()
              _tmpindex = _index
            else:
              if _tmpindex == _index-1:
                _title = _tmp.strip()
    if _email != []:
      info_dict["emails"].append(_email)
      info_dict["urls"].append(_url)
      info_dict["titles"].append(_title)
  return info_dict

def write_Email(_emailtemplate, input_List, _adress, _title):
  _senderName = input_List['Firstname']+' '+input_List['Lastname']
  _senderAddress = input_List['Email']

  with open('emailpassword.txt', mode='r') as f:
    _psswrd = f.readline().strip()
  html = Template(_emailtemplate.read_text())
  email = EmailMessage()
  email['from'] = _senderAddress
  email['to'] = _adress
  email['subject'] = "Interesse an Wohnung: "+_title

  email.set_content(html.substitute({'myname': input_List['Firstname']}), 'html')
  email.set_content(html.substitute({'mynumber': input_List['Telephone']}), 'html')
  email.set_content(html.substitute({'objecttitle': _title}), 'html')
  email.set_content(html.substitute({'myfullname': _senderName}), 'html')

  # 'smtp.gmail.com' for google
  # 'smtp.live.com' for hotmail
  with smtplib.SMTP(host="smtp.live.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_senderAddress, _psswrd)
    smtp.send_message(email)
    print('email sent!')
#
#
