import requests
from bs4 import BeautifulSoup
import re
#import pprint
#from fake_useragent import UserAgent
   

def gather_log_info_immobilienscout24(_url2scrape, filepath):
  res = requests.get(_url2scrape)

  #if res.status_code == 405:
  #  ua = UserAgent()
  #  header = {'User-Agent':str(ua.chrome)}
  #  htmlContent = requests.get(_url2scrape, headers=header)

  soup = BeautifulSoup(res.text, 'html.parser')

  with open(filepath, mode='w') as outfile:
    outfile.write('\n')
    try:
      outfile.write(soup.find('input', id='AnzeigenUeberschrift')['value'])
    except:
      pass
    outfile.write('\n\n')
    try:
      outfile.write(soup.find('span', class_='no_s').text)
    except:
      pass
    outfile.write('\n')
    try:
      outfile.write(soup.find('div', class_='merkmale').text)
    except:
      pass
    outfile.write('\n')
    try:
      price = soup.find_all('div', class_='hardfact')[0].text
      outfile.write(re.sub("\s{4,}"," ",price.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      area = soup.find_all('div', class_='hardfact')[1].text
      outfile.write(re.sub("\s{4,}"," ",area.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      rooms = soup.find('div', id='statusFacts').find('div', class_='hardfact rooms').text
      outfile.write(re.sub("\s{4,}"," ",rooms.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      overview_price = soup.find('div', class_='section preise odd').text
      outfile.write(re.sub("\s{4,}","\n\n ",overview_price.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      overview_immobilie = soup.find('div', id='divImmobilie').text
      outfile.write(re.sub("\s{4,}","\n\n ",overview_immobilie.strip()))
    except:
      pass
    outfile.write('\n')
  return True


def gather_log_info_immowelt(_url2scrape, filepath):
  res = requests.get(_url2scrape)
  soup = BeautifulSoup(res.text, 'html.parser')

  with open(filepath, mode='w') as outfile:
    outfile.write('\n')
    try:
      outfile.write(soup.find('input', id='AnzeigenUeberschrift')['value'])
    except:
      pass
    outfile.write('\n\n')
    try:
      outfile.write(soup.find('span', class_='no_s').text)
    except:
      pass
    outfile.write('\n')
    try:
      outfile.write(soup.find('div', class_='merkmale').text)
    except:
      pass
    outfile.write('\n')
    try:
      price = soup.find_all('div', class_='hardfact')[0].text
      outfile.write(re.sub("\s{4,}"," ",price.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      area = soup.find_all('div', class_='hardfact')[1].text
      outfile.write(re.sub("\s{4,}"," ",area.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      rooms = soup.find('div', id='statusFacts').find('div', class_='hardfact rooms').text
      outfile.write(re.sub("\s{4,}"," ",rooms.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      overview_price = soup.find('div', class_='section preise odd').text
      outfile.write(re.sub("\s{4,}","\n\n ",overview_price.strip()))
    except:
      pass
    outfile.write('\n')
    try:
      overview_immobilie = soup.find('div', id='divImmobilie').text
      outfile.write(re.sub("\s{4,}","\n\n ",overview_immobilie.strip()))
    except:
      pass
    outfile.write('\n')
  return True 


def gather_log_info_immobilienmarkt_sueddeutsche(_url2scrape, filepath):
  res = requests.get(_url2scrape)
  soup = BeautifulSoup(res.text, 'html.parser')

  with open(filepath, mode='w') as outfile:
    outfile.write('\n')
    try:
      main1 = soup.find('div', class_='exposeMain').text
      outfile.write(re.sub("\s{4,}"," ",main1.strip()))
    except:
      pass
    outfile.write('\n\n')
    try:
      main1 = soup.find('div', class_='exposeFactBox').text
      outfile.write(re.sub("\s{4,}"," ",main1.strip()))
    except:
      pass
    outfile.write('\n\n')
    try:
      for str_i in soup.find_all('div', class_='hidebox open'):
        outfile.write(re.sub("\s{4,}"," ",str_i.text))
    except:
      pass
    outfile.write('\n\n')
  return True 
#