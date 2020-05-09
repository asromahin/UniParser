from src.elements.element import UniElement
import src.constants as constants


class UniPaginator(UniElement):

    def __init__(self, browser, elem=None):
        super(UniPaginator, self).__init__(browser, elem)
        self.update()

    def parse_paginator(self):
        res = []
        for key in constants.PAGINATOR_LINKS:
            paginators = self.elem.find_elements_by_attrs(attrs=key, is_sim=False, is_recurse=True)
            if paginators:
                res.extend(paginators)
                return res
        return res

    def get_current_page(self):
        for i, elem in enumerate(self.paginator_elems):
            active_elem = elem.find_elements_by_attrs({'class': 'active'}, is_sim=False, is_children=False)
            if active_elem:
                return i

    def update(self):
        super().update()
        self.paginator_elems = self.parse_paginator()
        self.current_elem = self.get_current_page()


    def __get_type_paginator(self):
        pass

    def to_pos(self, pos):
        pass

    def next(self):
        if self.paginator_elems:
            new_index = self.current_elem+1
            if new_index < len(self.paginator_elems):
                self.browser.click(self.paginator_elems[new_index])
                #self.browser.get_stable_tree([self], interval=0.3)
                self.browser.get_stable_page(interval=0.3)
                #self.browser.reinit()
                return True
            else:
                return False
        else:
            return False


    def prev(self):
        pass