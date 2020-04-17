from src.utils import delete_parents, get_tree_attr_value
from src.constants import LIST_PAGINATION_ATTRS
from bs4 import BeautifulSoup


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
        self.table_elem = table_elem

        self.rows_tag = rows_tag
        self.columns_tag = columns_tag

        if self.rows_tag:
            self.rows = self.get_rows(self.table_elem, self.rows_tag)
        if self.columns_tag:
            if self.rows:
                self.rows_data = []
                for row in self.rows:
                    columns = self.get_columns(row, columns_tag)
                    self.rows_data.append(columns)

    def get_rows(self, table, rows_name):
        return table.find_elements_by_tag_name(rows_name)

    def get_columns(self, row, columns_name):
        return row.find_elements_by_tag_name(columns_name)

    def to_df(self):
        res_df = []
        for i, row in enumerate(self.rows_data):
            row_data = {}
            href = get_tree_attr_value(self.rows[i], 'href')
            if href:
                row_data['href'] = href
            for column in row:
                if column.text:
                    row_data[column.get_attribute('class')+"_text"] = column.text
            res_df.append(row_data)
        return res_df


