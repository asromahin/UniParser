from src.parser import PageParser
from src.utils import screen_elem, get_wd_xpath
import time

parser = PageParser(src_wd='webdriver/chromedriver.exe', is_hide=True)
parser.get_page('https://game-tournaments.com/lol')
#time.sleep(1)
#print(parser.analyze_page())
print(parser.wd.title)
#print(parser.find_tables()[-1].to_df().to_csv('result.csv'))

#curtime = time.time()
test_elem = parser.wd.find_elements_by_tag_name('div')[-1]
#print(time.time()-curtime)


test_xpath = get_wd_xpath(test_elem)

#curtime = time.time()
result_elem = parser.wd.find_element_by_xpath(test_xpath)
#print(time.time()-curtime)


print(test_xpath)
print(test_elem)
print(result_elem)
print(result_elem == test_elem)