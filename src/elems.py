from src.utils import delete_parents, get_tree_attr_value, filter_string
from src.constants import DATA_PARSER

from bs4 import BeautifulSoup
import pandas as pd


class UniElem():

    def __init__(self, wd, isreinit_elem=False):
        self.wd = wd
        self.isreinit_elem = isreinit_elem

    def valid_elem(self):
        try:
            self.elem
            return True
        except:
            #print('empty elem')
            return False

    def reinit(self):
        if(self.valid_elem):
            if(self.isreinit_elem):
                self.reinit_element()

    def reinit_element(self):
        soup_elem = BeautifulSoup(self.elem.get_attribute('innerHTML'), 'html.parser')

        tag_elems = self.wd.find_elements_by_tag_name(soup_elem.tag)

        for elem in tag_elems:
            trig = True
            for attr in soup_elem.attrs:
                value = elem.get_attribute(attr)
                if not value:
                    trig = False

            if trig:
                self.elem = elem
                break


class UniPaginator(UniElem):

    def __init__(self, wd, next_format=None, current_page=0, isscript=False):

        super().__init__(wd)
        self.next_format = next_format
        self.current_page = current_page
        self.isscript = isscript

    def open_page(self, page):
        next = self.next_format.format(page)
        if self.isscript:
            self.wd.execute_script(next)
        else:
            self.wd.get(self.next_format)
        self.current_page = page

    def next_page(self):
        self.open_page(self.current_page+1)


class UniTable(UniElem):

    def __init__(self, wd, table_elem, rows_tag=None, columns_tag=None):
        super().__init__(wd, isreinit_elem=True)

        self.rows_tag = rows_tag
        self.columns_tag = columns_tag

        self.reinit(table_elem)

    def reinit(self, new_table):

        super().reinit()

        self.elem = new_table
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
        return pd.DataFrame(res_df)

class UniData(UniElem):
    def __init__(self, wd, elem):
        super().__init__(wd, isreinit_elem=True)
        self.elem = elem

    def reinit(self):
        super().reinit()

    def get_data(self):
        result = {}
        soup_elem = BeautifulSoup(self.elem.get_attribute('innerHTML'), 'html.parser')
        children = soup_elem.getChildren(recursive=True)
        for child in children:
            for attr in DATA_PARSER:
                if(attr in child.attrs):
                    result[attr]=child[attr]

            text_data = child.getText()
            if(text_data):
                result['text'] = text_data
        return result








