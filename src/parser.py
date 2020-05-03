from src.utils import init_wd, get_wd_all_tags
from src.elems import UniTable
from src.constants import TABLES_KEYS

class PageParser():

    def __init__(self, src_wd='chromedriver', is_hide=True):
        self.wd = init_wd(src_wd, is_hide)
        self.tables = []

    def get_page(self, url):
        self.wd.get(url)

        self.tables = self.find_tables()

    def analyze_page(self):
        analyze_data = {}
        all_tags = get_wd_all_tags(self.wd)
        for tag in all_tags:
            analyze_data[tag] = len(self.wd.find_elements_by_tag_name(tag))
        return analyze_data

    def find_tables(self, isfilter=True):
        for table_key in TABLES_KEYS['table']:
            tables = self.wd.find_elements_by_tag_name(table_key)
            if tables:
                break
        res_tables = []
        for table in tables:
            utable = UniTable(self.wd, table, 'tr', 'td')
            res_tables.append(utable)
        if isfilter:
            res_tables = self.filter_tables(res_tables)
        return res_tables

    def filter_tables(self, tables):
        return tables


