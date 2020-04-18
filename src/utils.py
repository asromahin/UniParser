from selenium import webdriver
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from src.constants import LIST_PAGINATION_ATTRS, FILTERED_SYMBOLS

def init_wd():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    wd = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    return wd



def delete_parents(elems):
  delete_elems=[]
  for elem in elems:
    children = elem.findChildren(recursive=True)
    for elem_check in elems:
      for child in children:
        if(elem_check==child):
          delete_elems.append(elem)
          break
    for del_elem in delete_elems:
      elems.remove(del_elem)
    return elems

def get_tree_attrs(elem):
    soup = BeautifulSoup(elem, 'html.parser')
    children = soup.findChildren(recursive=True)
    all_attrs = []
    for child in children:
        all_attrs.expand(child.attrs)
    all_attrs = list(set(all_attrs))
    return all_attrs

def get_tree_attr_value(elem,attribute):
    soup = BeautifulSoup(elem, 'html.parser')
    children = soup.findChildren(recursive=True)
    all_attrs = []
    for child in children:
        if(attribute in child.attrs):
            return child[attribute]
    return None

def filter_string(str):
    for symbol in FILTERED_SYMBOLS:
        str = str.replace(symbol, '')
    str = str.strip()
    return str

def get_wd_tag(elem):
    return elem.get_attribute('outerHTML').split(' ', 1)[0].replace('<', '').replace('>', '').strip()

def get_wd_attrs(elem):
    return elem.get_attribute('outerHTML').split(' ', 1)[0].replace('<', '').replace('>', '').strip()