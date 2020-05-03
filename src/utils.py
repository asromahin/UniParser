from selenium import webdriver
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from src.constants import LIST_PAGINATION_ATTRS, FILTERED_SYMBOLS

def init_wd(src_wd='chromedriver', is_hide=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    if is_hide:
        wd = webdriver.Chrome(src_wd, chrome_options=chrome_options)
    else:
        wd = webdriver.Chrome(src_wd)
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

def get_wd_all_tags(elem):
    soup = BeautifulSoup(elem.page_source, 'html.parser')
    children = soup.findChildren(recursive=True)
    all_tags = []
    for child in children:
        all_tags.append(child.name)
    all_tags = list(set(all_tags))
    return all_tags

def screen_elem(elem, filename):
    element_png = elem.screenshot_as_png
    with open(filename, "wb") as file:
        file.write(element_png)

def get_wd_xpath(elem):
    xpath = []
    is_last = False
    while not is_last:
        elem_tag = get_wd_tag(elem)
        try:
            parent_elem = elem.find_element_by_xpath('..')
        except:
            is_last = True
        if not is_last:
            parents_children = parent_elem.find_elements_by_xpath(f'../*')
            if len(parents_children) != 1:
                index = 0
                counter = 0
                for i, child in enumerate(parents_children):
                    if get_wd_tag(child) == elem_tag:
                        counter += 1
                        if child == elem:
                            index = counter
                if counter > 1:
                    elem_tag = elem_tag + f'[{index+1}]'
        xpath.append(elem_tag)
        elem = parent_elem
    xpath.append('')
    return '/'.join(xpath[::-1])