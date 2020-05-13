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
'https://mebelars.ru/catalog/ofisnye-stoly.html'


curtime = time.time()
parser = UniWebBrowser(url='https://game-tournaments.com/lol', src_wd='webdriver/chromedriver.exe', is_hide=True,
                       is_find_elements=True)

print(parser.paginators)

select_index = None
for i, pagin in enumerate(parser.paginators):
    print(pagin.current_page)
    print(pagin.elem.data)
    if pagin.elem.xpath:
        if pagin.current_page != None:
           select_index = i
           break

print('?'*40)
print(select_index)
print('?'*40)
#for pagin in parser.paginators[-1].paginator_elems:
 #   print(pagin.text)

print(parser.paginators[select_index].current_page)

print(time.time()-curtime)
start = UniBehaviourStart(parser)
start.add(UniBehaviourMovePaginator(parser, parser.paginators[select_index], changed_size=2))

res = start.move()
#res.to_csv('res.csv')
lens_res = []
for key in res.keys():
    lens_res.append(len(res[key]))
print(list(set(lens_res)))

pd.DataFrame(res).to_csv('res.csv')

parser.quit()