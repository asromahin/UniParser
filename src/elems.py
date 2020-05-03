from src.utils import delete_parents, get_tree_attr_value, filter_string, get_wd_tag, screen_elem, get_wd_xpath
from src.constants import DATA_PARSER

from bs4 import BeautifulSoup
import pandas as pd


class UniElem():

    def __init__(self, wd, elem=None, isreinit_elem=True):
        self.wd = wd
        self.isreinit_elem = isreinit_elem
        self.elem = elem
        if self.elem:
            self.tag_elem = get_wd_tag(self.elem)
            soup_elem = BeautifulSoup(self.elem.get_attribute('innerHTML'), 'html.parser')
            self.attrs_elem = soup_elem.attrs
            self.xpath = get_wd_xpath(self.elem)
            self.__reinit()

    def valid_elem(self):
        return 'elem' in dir(self)

    def __reinit(self):
        if self.xpath:
            self.elem = self.wd.find_element_by_xpath(self.xpath)
        self.reinit()

    def reinit(self):
        pass

    def save_as_screen(self, screen_name):
        if(self.elem):
            self.wd.set_window_size(self.elem.size['width'], self.elem.size['height'])
            screen_elem(self.elem, screen_name)


class DataElem(UniElem):

    def __init__(self, wd, elem, attr_keys=[]):
        super().__init__(wd=wd, elem=elem)
        self.attr_keys = attr_keys
        self.get_data()

    def get_data(self):
        res_data = {}
        if self.attr_keys:
            for key in self.attr_keys:
                key_data = self.elem.get_attribute(key)
                res_data[key] = key_data
        else:
            text_data = self.elem.getText()
            res_data['text'] = text_data
        self.data = res_data
        return res_data

    def reinit(self):
        self.get_data()




class UniPaginator(UniElem):

    def __init__(self, wd, next_format=None, current_page=0, isscript=False):

        super().__init__(wd)
        self.next_format = next_format
        self.current_page = current_page
        self.isscript = isscript

    def select_page(self, page):
        next = self.next_format.format(page)
        if self.isscript:
            self.wd.execute_script(next)
        else:
            self.wd.get(self.next_format)
        self.current_page = page

    def next_page(self):
        self.select_page(self.current_page+1)


class UniTable(UniElem):

    def __init__(self, wd, table_elem, rows_tag=None, columns_tag=None):
        super().__init__(wd, table_elem, isreinit_elem=True)

        self.rows_tag = rows_tag
        self.columns_tag = columns_tag

        self.reinit()

    def reinit(self):

        soup_elem = BeautifulSoup(self.elem.get_attribute('innerHTML'), 'html.parser')

        if self.rows_tag:
            self.rows = self.get_rows(soup_elem, self.rows_tag)
        if self.columns_tag:
            if self.rows:
                self.rows_data = []
                for row in self.rows:
                    columns = self.get_columns(row, self.columns_tag)
                    if columns:
                        self.rows_data.append(columns)

    def get_rows(self, table, rows_name):
        return table.find_all(rows_name)

    def get_columns(self, row, columns_name):
        return row.find_all(columns_name)

    def to_df(self, skip_columns=[], skip_rows=[]):
        res_df = []
        row_data = {}
        for i in range(len(self.rows_data)):
            if not i in skip_rows:
                row = self.rows_data[i]
                for j in range(len(row)):
                    if not j in skip_columns:
                        text_data = row[j].getText()
                        if text_data:
                            row_data[str(j)+"_text"] = filter_string(text_data)
                res_df.append(row_data.copy())
        return pd.DataFrame(res_df)#.drop(labels=[None], axis=0, index=None, columns=None, level=None, inplace=False, errors='raise')

class UniData(UniElem):
    def __init__(self, wd, elem):
        super().__init__(wd, elem=elem, isreinit_elem=True)

    def get_data(self):
        result = {}
        soup_elem = BeautifulSoup(self.elem.get_attribute('innerHTML'), 'html.parser')
        children = soup_elem.findChildren(recursive=True)
        children.append(soup_elem)
        for child in children:
            for attr in DATA_PARSER:
                if(attr in child.attrs):
                    result[attr] = filter_string(child[attr])

            text_data = child.getText()
            if(text_data):
                result['text'] = filter_string(text_data)
        return result








