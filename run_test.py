from src.browser.browser import UniWebBrowser
import os
import time

from src.behaviour.behaviour import UniBehaviourStart, UniBehaviourMovePaginator


'https://www.worldometers.info/ru/'
'https://vk.com'
'https://game-tournaments.com/lol'
'https://www.avito.ru/moskva'
'https://www.avito.ru/moskva/avtomobili?radius=0'


curtime = time.time()
parser = UniWebBrowser(url='https://game-tournaments.com/lol', src_wd='webdriver/chromedriver.exe', is_hide=False,
                       is_find_elements=True)
print(time.time()-curtime)
start = UniBehaviourStart(parser)
start.set_child(UniBehaviourMovePaginator(parser, parser.paginators[0], max_page=5))

res = start.move()

df = res[list(res.keys())[0]].to_csv('result.csv')
