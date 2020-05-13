from src.elements.element import UniElement
import src.constants as constants
import time

class UniPaginator(UniElement):

    def __init__(self, browser, elem=None):
        super(UniPaginator, self).__init__(browser, elem)
        self.current_page = None
        self.update()


    def parse_paginator(self):
        res = []
        #for key in constants.PAGINATOR_LINKS:
            #paginators = self.elem.find_elements_by_attrs(attrs=key, is_sim=False, is_recurse=True)
        paginators = self.elem.get_children(is_recurse=True)
        if paginators:
            #print(paginators)
            #print(paginators[0].data)
            #print(paginators[0].data['text'])
            res.extend(paginators)
            #return res
        #print('='*40)
        #print(len(res))
        res = list(set(res))
        #print(len(res))
        #print('=' * 40)
        return res

    def get_current_page(self):
        for i, elem in enumerate(self.paginator_elems):
            for key in constants.PAGINATOR_CURRENT:
                active_elem = elem.find_elements_by_attrs(key, is_sim=False, is_children=False)
                if active_elem:
                    #print(active_elem)
                    #print(active_elem[0].data)
                    try:
                        #print(active_elem[0].text)
                        self.current_page = int(active_elem[0].text)
                        return elem
                    except:
                        #self.current_page = None
                        return None

    def get_next_page(self):
        cur_elem = self.get_current_page()
        for i, elem in enumerate(self.paginator_elems):
            #print(elem.data)
            try:
                if int(elem.text) == int(cur_elem.text)+1:
                    return elem
            except:
                pass
        return None

    def get_prev_page(self):
        cur_elem = self.get_current_page()
        for i, elem in enumerate(self.paginator_elems):
            # print(elem.data)
            try:
                if int(elem.text) == int(cur_elem.text) - 1:
                    return elem
            except:
                pass
        return None


    def update(self):
        super().update()
        self.paginator_elems = self.parse_paginator()
        self.current_elem = self.get_current_page()


    def __get_type_paginator(self):
        pass

    def to_pos(self, pos):
        if pos > self.current_page:
            self.next()
            self.to_pos(pos)
        elif pos < self.current_page:
            self.prev()
            self.to_pos(pos)
        else:
            return True

    def next(self):
        if self.paginator_elems:
            new_elem = self.get_next_page()
            if new_elem:
                start_time = time.time()
                print(new_elem.data)
                self.browser.click(new_elem)
                #self.browser.get_stable_tree([self], interval=0.3)
                self.browser.get_stable_page(interval=0.3)
                #self.browser.reinit()
                print('next')
                print('page=', self.current_page)
                print('time=', time.time()-start_time)
                return True
            else:
                return False
        else:
            return False


    def prev(self):
        if self.paginator_elems:
            new_elem = self.get_prev_page()
            if new_elem:
                start_time = time.time()
                self.browser.click(new_elem)
                # self.browser.get_stable_tree([self], interval=0.3)
                self.browser.get_stable_page(interval=0.3)
                # self.browser.reinit()
                print('prev')
                print('page=', self.current_page)
                print('time=', time.time()-start_time)
                return True
            else:
                return False
        else:
            return False