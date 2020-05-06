from src.elements.element import UniElement
import src.constants as constants


class UniPaginator(UniElement):

    def __init__(self, browser, elem=None, start_elem=0):
        super(UniPaginator, self).__init__(browser, elem)
        self.paginator_elems = self.parse_paginator()
        self.current_elem = start_elem

    def parse_paginator(self):
        res = []
        for key in constants.PAGINATOR_LINKS:
            paginators = self.elem.find_elements_by_attrs(attrs=key, is_sim=False, is_recurse=True)
            if paginators:
                res.extend(paginators)
                return res
        return res

    def __get_type_paginator(self):
        pass

    def to_pos(self, pos):
        pass

    def next(self):
        if self.paginator_elems:
            self.browser.click(self.paginator_elems[2])
            self.browser.get_stable_page(interval=0.2)
            self.browser.reinit()


    def prev(self):
        pass