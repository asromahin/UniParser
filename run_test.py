from src.browser.browser import UniWebBrowser
import os
import time
import pandas as pd

from src.behaviour.behaviour import UniBehaviourStart, UniBehaviourMovePaginator


'https://www.worldometers.info/ru/'
'https://vk.com'
'https://game-tournaments.com/lol'
'https://www.avito.ru/moskva'
'https://www.avito.ru/moskva/avtomobili?radius=0'
'https://mebelars.ru/catalog/kresla-dlya-personala.html'


curtime = time.time()
parser = UniWebBrowser(url='https://mebelars.ru/catalog/kresla-dlya-personala.html', src_wd='webdriver/chromedriver.exe', is_hide=True,
                       is_find_elements=True)
print(time.time()-curtime)
start = UniBehaviourStart(parser)
start.add(UniBehaviourMovePaginator(parser, parser.paginators[0], changed_size=2))

res = start.move()
#res.to_csv('res.csv')
lens_res = []
for key in res.keys():
    lens_res.append(len(res[key]))
print(list(set(lens_res)))

pd.DataFrame(res).to_csv('res.csv')

parser.quit()