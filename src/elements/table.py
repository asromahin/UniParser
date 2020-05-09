from src.elements.element import UniElement
import src.constants as constants

class UniTable(UniElement):
    def __init__(self, browser, elem=None, row_tag=None, column_tag=None):
        super(UniTable, self).__init__(browser, elem)
        self.row_tag = row_tag
        self.column_tag = column_tag

        if not row_tag and not column_tag:
            self.table = self.get_table(row_tag=constants.KEY_TABLE_ROW, column_tag=constants.KEY_TABLE_COLUMN)
        elif row_tag and column_tag:
            self.table = self.get_table(row_tag=row_tag, column_tag=column_tag)

        self.table_data = self.get_table_data()

    def __get_by_tag_keys(self, elem, keys):
        for key in keys:
            result = elem.find_elements_by_tag_name(key)
            if result:
                return result
        return []

    def get_table(self, row_tag, column_tag):
        table = []
        rows = self.__get_by_tag_keys(self.elem, row_tag)
        for row in rows:
            uni_row = UniTableRow(self.browser, row, column_tag=column_tag)
            table.append(uni_row)
        return table

    def get_table_data(self):
        res = []
        for row in self.table:
            res.append(row.get_data())
        return res


class UniTableRow(UniElement):
    def __init__(self, browser, elem=None, column_tag=None):
        super(UniTableRow, self).__init__(browser, elem)
        self.column_tag = column_tag
        self.columns = self.get_columns(self.column_tag)

    def get_columns(self, column_tag):
        return self.__get_by_tag_keys(self.elem, column_tag)

    def get_data(self):
        res = []
        res.extend(self.elem.get_refs())
        for column in self.columns:
            res.append(column.text)
        return res

    def __get_by_tag_keys(self, elem, keys):
        for key in keys:
            result = elem.find_elements_by_tag_name(key)
            if result:
                return result
        return []

