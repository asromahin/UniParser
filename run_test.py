from src.browser.browser import UniWebBrowser
import os
import time


'https://www.worldometers.info/ru/'
'https://vk.com'
'https://game-tournaments.com/lol'
'https://www.avito.ru/moskva'
'https://www.avito.ru/moskva/avtomobili?radius=0'


curtime = time.time()
parser = UniWebBrowser(url='https://www.avito.ru/moskva/avtomobili?radius=0', src_wd='webdriver/chromedriver.exe', is_hide=True,
                       is_find_elements=True)

print(time.time()-curtime)
print(parser.images)
for image in parser.images:
    try:
        print(image.elem.get_selenium_element(parser.wd).get_attribute('outerHTML'))
    except:
        print('error')
print(parser.paginators)
print(parser.tables)
#parser.quit()