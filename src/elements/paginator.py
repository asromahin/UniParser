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
        print(self.paginator_elems)
        print('-'*60)
        for i, elem in enumerate(self.paginator_elems):
            #print(elem.parent.attrs)
            if 'class' in elem.parent.attrs.keys():
                if elem.parent.attrs['class'] == ['active']:
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
        print('NEXT'*20)
        if self.paginator_elems:
            new_index = self.current_elem+1
            if new_index < len(self.paginator_elems):
                self.browser.click(self.paginator_elems[new_index])
                print('TOCLICK' * 20)
                self.browser.get_stable_page(interval=0.5)
                print('TOSTABLE' * 20)
                return True
            else:
                return False
        else:
            return False


    def prev(self):
        pass