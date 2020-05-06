from selenium import webdriver
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

import src.constants as constants

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

def filter_string(str):
    for symbol in constants.FILTERED_SYMBOLS:
        str = str.replace(symbol, '')
    str = str.strip()
    return str