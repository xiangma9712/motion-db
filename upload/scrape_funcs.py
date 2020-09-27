import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def refineRound(text,tab = "tabby"):
  if "ラウンド" in text:
    return text.replace("ラウンド","")

  if "Round" in text:
    return text.replace("Round ","")

  swap_pair = {"Open ":"",
               "Octofinals":"OF",
               "Quarterfinals":"QF",
               "Semifinals":"SF",
               "Grand Final":"GF",
               "Partial Double-":"Pre ",
               "Finals" :"GF",
               "Double quarterfinals":"Pre QF",
               "Open":""
               }

  for k, v in swap_pair.items():
    if k in text:
      text = text.replace(k,v)

  if not tab == "tabby" and "Rookie" in text:
      text = "Rookie " + text.replace("Rookie","")

  return text

def urlBuilder(input_url):
  url_splited = input_url.split("/")
  #case : tabby cat
  if "herokuapp.com" in input_url:
    if url_splited[0] == "https:":
        url = "/".join(url_splited[0:4])
    else:
        url = "https://" + "/".join(url_splited[0:2])

    url += "/motions/statistics/"
    return url

  #case : tabbr
  if "tabbr" in input_url:
    if url_splited[0] == "https:":
      url = "/".join(url_splited[0:5])
    else:
      url = "https://" + "/".join(url_splited[0:3])

    url += "/motions/"
    return url

  #case : unkown
  return None

def scrape_tabbyCat_BP(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  divs = soup.find_all("div",{'class': 'list-group mt-3'})
  motions = {}
  for each in divs:
    motion = each.h4.get_text(strip=True)
    meta = refineRound(each.span.string)
    info = ""
    try:
      info = each.find("div",{'class': 'modal-body lead'}).get_text(strip=True)
    except:
      pass
    motions[meta] = [motion,info]

  return motions

def scrape_tabbyCat_Asian(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  divs = soup.find_all("div",{'class': 'list-group mt-3'})
  motions = {}
  for each in divs:
    motion_texts = each.find_all("h4")
    meta = refineRound(each.span.string)
    motion_set = []
    for m in motion_texts:
      info = ""
      try:
        info = m.find("div",{'class': 'modal-body lead'}).get_text(strip=True)
      except:
        pass
      motion_set.append([m.get_text(strip=True),info])

    motions[meta] = motion_set

  return motions

def scrape_tabbr(url):
  options = Options()
  options.add_argument('--headless')
  driver = webdriver.Chrome(options=options)
  driver.get(url)
  WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jss304')))
  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html)
  boxs = soup.find_all("div",{"class":"jss191 jss193 jss192 jss345 jss342"})
  motions = {}
  for each in boxs:
    rounds = refineRound(each.div.div.get_text(strip = True),tab="tabbr")
    m_set_row = each.find_all("div",{"class":"jss370"})
    m_set = []
    for m in m_set_row:
      motion_text = m.span.get_text(strip = True)
      info = ""
      try:
          info = m.p.get_text(strip = True)
      except:
          pass
      m_set.append([motion_text,info])

    motions[rounds] = m_set

  del motions["Quick tip"]
  return motions

def scrape(input_url, asian=False):
  url = urlBuilder(input_url)
  if url == None:
    return None

  #case : BP
  if not asian:
    return scrape_tabbyCat_BP(url)

  #case : tabbr
  if "tabbr" in url:
    return scrape_tabbr(url)

  #case : tabbyCat Asian
  return scrape_tabbyCat_Asian(url)
