from src.utils import delete_parents, get_tree_attr_value, filter_string

from bs4 import BeautifulSoup
import pandas as pd


class UniElem():

    def __init__(self, wd):
        self.wd = wd


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
        super().__init__(wd)

        self.rows_tag = rows_tag
        self.columns_tag = columns_tag

        self.reinit(table_elem)

    def reinit(self, new_table):

        self.table_elem = new_table
        self.table_elem = BeautifulSoup(self.table_elem.get_attribute('innerHTML'), 'html.parser')

        print(len(self.table_elem.find_all({'data-ref': True})))

        if self.rows_tag:
            self.rows = self.get_rows(self.table_elem, self.rows_tag)
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

    def to_df(self):
        res_df = []
        row_data = {}
        for i in range(len(self.rows_data)):
            row = self.rows_data[i]
            for j in range(len(row)):
                text_data = row[j].getText()
                if text_data:
                    row_data[str(j)+"_text"] = filter_string(text_data)
            res_df.append(row_data.copy())
        return pd.DataFrame(res_df)






