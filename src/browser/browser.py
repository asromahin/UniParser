from src.elements.node import UniNode
from src.elements.table import UniTable
from src.elements.paginator import UniPaginator
from src.elements.image_container import UniImageContainer
import src.constants as constants
from src.utils.utils import init_wd

from bs4 import BeautifulSoup

import time

class UniWebBrowser(UniNode):

    def __init__(self, url=None, src_wd='chromedriver', is_hide=True, is_find_elements=False):

        self.wd = init_wd(src_wd=src_wd, is_hide=is_hide)
        self.history = UniWebBrowserHistory(self.wd)

        self.is_hide = is_hide
        self.is_find_elements = is_find_elements

        if url:
            self.get_page(url=url)

            self.reinit()

    def get_page(self, url):
        start_time = time.time()
        self.wd.get(url)
        end_time = time.time() - start_time
        self.url = url
        self.history.set_url(url, end_time)

    def quit(self):
        self.wd.quit()

    def click(self, element):
        self.wd.find_element_by_xpath(element.xpath).click()

    def send_keys(self, element, keys):
        self.wd.find_element_by_xpath(element.xpath).send_keys(keys)

    def screen_element(self, element, save_path=None):
        selen_elem = self.wd.find_element_by_xpath(element.xpath)
        self.wd.set_window_size(selen_elem.size['width'], selen_elem.size['height'])
        screen = selen_elem.screenshot_as_png
        if save_path:
            with open(save_path, "wb") as file:
                file.write(screen)
        return screen


    def reinit(self):
        self.soup = BeautifulSoup(self.wd.page_source, 'html.parser')
        super(UniWebBrowser, self).__init__(self.soup)
        self.elements = self.get_children(is_recurse=True)

        if self.is_find_elements:
            self.tables = self.find_tables()

            self.paginators = self.find_paginators()

            self.images = self.find_images()

    def listen(self, interval=1, max_timer=None):
        start_timer = time.time()
        while True:
            time.sleep(interval)
            if self.is_changed_page():
                soup = BeautifulSoup(self.wd.page_source, 'html.parser')
                ctime = time.time()
                new_node = UniNode(soup)
                diff = self.get_difference(new_node)
                print(time.time()-ctime, len(diff[0]), len(diff[1]), len(diff[2]))
                cur_time = time.time() - start_timer
                if max_timer:
                    if cur_time > max_timer:
                        return None
                #self.reinit()


    def is_changed_page(self):
        soup = BeautifulSoup(self.wd.page_source, 'html.parser')
        res = (soup != self.soup)
        return res

    def get_stable_page(self, interval=0.5, max_timer=10):

        soup = BeautifulSoup(self.wd.page_source, 'html.parser')
        start_timer = time.time()
        time.sleep(interval)
        while self.is_changed_page():

            cur_time = time.time() - start_timer
            if cur_time > max_timer:
                return None
            time.sleep(interval)
            self.reinit()

        return soup

    def find_tables(self):
        collect_tables = []
        res = []
        for tag in constants.KEY_TABLE:
            tables = self.find_elements_by_tag_name(tag)
            if tables:
                collect_tables.extend(tables)
        for table in collect_tables:
            res.append(UniTable(self, table))
        return res

    def find_paginators(self):
        collect_paginators = []
        res = []
        for key in constants.KEY_PAGINATOR:
            paginators = self.find_elements_by_attrs(key, is_sim=False)
            if paginators:
                collect_paginators.extend(paginators)
        for key in constants.KEY_PAGINATOR_TAG:
            paginators = self.find_elements_by_tag_name(key)
            if paginators:
                collect_paginators.extend(paginators)
        for pagin in paginators:
            res.append(UniPaginator(self, pagin))
        return res

    def find_images(self):
        res = []
        res_images = []
        for key in constants.KEY_IMAGES:
            images = self.find_elements_by_tag_name(key, is_sim=True)
            res_images.extend(images)
        for image in res_images:
            image_container = UniImageContainer(self, image)
            res.append(image_container)
        return res

    def scroll_page(self, is_recurse=True):
        last_height = self.wd.execute_script("return document.body.scrollHeight")
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.get_stable_page(interval=0.3)
        new_height = self.wd.execute_script("return document.body.scrollHeight")
        print(new_height)
        if is_recurse:
            if new_height > last_height:
                self.scroll_page()
            else:
                self.reinit()
        else:
            self.reinit()


class UniWebBrowserHistory():

    def __init__(self, browser):
        self.browser = browser
        self.history = {
            'url': [],
        }

    def set_history(self, key, value):
        if key in self.history.keys():
            self.history[key].append(value)
        else:
            self.history[key] = [value]

    def set_url(self, url, time_wait=None):
        self.set_history(key='url', value=url)
        self.set_history(key='time_wait', value=time_wait)