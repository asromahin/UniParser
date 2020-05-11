import pandas as pd
from tqdm import tqdm

class UniBehaviour():

    def __init__(self, browser):
        self.browser = browser
        self.child = None
        self.parent = None
        self.parse_elems = []

    def set_parse_elems(self, elems):
        self.parse_elems = elems

    def set_child(self, behaviour):
        self.child = behaviour
        self.child.parent = self

    def add(self, behaviour):
        if self.child:
            self.child.add(behaviour)
        else:
            self.set_child(behaviour)

    def insert_child(self, behaviour):
        print(behaviour)
        buf_child = self.child
        print(buf_child)
        self.set_child(behaviour)
        buf_child.parent = self.child


    def move(self, result={}):
        result = self.get_data(result)
        if self.child:
            return self.child.move(result)
        else:
            return result

    """def get_data(self, result={}):
        for table in self.browser.tables:
            if table.elem.xpath in result.keys():
                result[table.elem.xpath] = pd.concat([result[table.elem.xpath], pd.DataFrame(table.data)])
            else:
                result[table.elem.xpath] = pd.DataFrame(table.data)
        return result"""

    def get_data(self, result={}):
        new_result = result.copy()
        for elem in self.parse_elems:
            try:
                if not elem.xpath in new_result.keys():
                    new_result[elem.xpath] = [elem.text]
                    for ref_key in elem.refs.keys():
                        new_result[elem.xpath+ref_key] = elem.refs[ref_key]
                else:
                    new_result[elem.xpath].append(elem.text)
                    for ref_key in elem.refs.keys():
                        new_result[elem.xpath + ref_key].append(elem.refs[ref_key])
            except:
                new_result = result
                break
        return new_result

    def update(self):
        for i in range(len(self.parse_elems)):
            try:
                self.parse_elems[i] = self.browser.find_element_by_xpath(self.parse_elems[i].xpath)
            except:
                pass


class UniBehaviourStart(UniBehaviour):

    def __init__(self, browser):
        super(UniBehaviourStart, self).__init__(browser=browser)


class UniBehaviourMovePaginator(UniBehaviour):

    def __init__(self, browser, paginator, changed_size=2, max_page=None):
        super(UniBehaviourMovePaginator, self).__init__(browser=browser)
        self.paginator = paginator
        self.max_page = max_page
        self.changed_size = changed_size
        finding_elems = self.find_changed_elements()
        self.set_parse_elems(finding_elems)

    def move(self, result={}):
        is_next = self.paginator.next()
        result = self.get_data(result)
        self.update()
        while is_next:
            #print(is_next, self.paginator, self.paginator.elem)
            is_next = self.paginator.next()
            if is_next:
                result = self.get_data(result)
            self.update()
            if self.max_page:
                if self.paginator.current_page >= self.max_page:
                    break
        return result

    def find_changed_elements(self):
        node_list = []

        start_pos = self.paginator.current_page
        for i in tqdm(range(self.changed_size)):
            self.paginator.next()
            node_list.append(self.browser.copy())

        self.paginator.to_pos(start_pos)

        changed, miss, new = node_list[0].get_difference(node_list[1])
        for i, node in enumerate(node_list[1:-1]):
            nchanged, nmiss, nnew = node.get_difference(node_list[i+1])
            changed.extend(nchanged)
            #miss.extend(nmiss)
            #new.extend(nnew)
        #changed = list(set(changed))
        #miss = list(set(miss))
        #new = list(set(new))
        return changed




class UniBehaviourMoveRefs(UniBehaviour):

    def __init__(self, browser, refs, changed_size=2, ref_prefix=None, max_refs=None):
        super(UniBehaviourMovePaginator, self).__init__(browser=browser)
        self.refs = refs
        self.ref_prefix = ref_prefix
        self.max_refs = max_refs
        self.changed_size = changed_size

    def move(self, result={}):
        for ref in tqdm(self.refs):
            if self.ref_prefix:
                ref = self.ref_prefix+ref
            self.browser.get_page(ref)
            result = self.get_data(result)
            self.browser.get_stable_page(interval=0.3)
        return result

    def find_changed_elements(self):
        node_list = []
        for i in tqdm(range(self.changed_size)):
            ref = self.refs[i]
            if self.ref_prefix:
                ref = self.ref_prefix+ref
            self.browser.get_page(ref)
            node_list.append(self.browser.copy())

        changed, miss, new = node_list[0].get_difference(node_list[1])
        for i, node in enumerate(node_list[1:-1]):
            nchanged, nmiss, nnew = node.get_difference(node_list[i+1])
            changed.extend(nchanged)
            #miss.extend(nmiss)
            #new.extend(nnew)
        changed = list(set(changed))
        #miss = list(set(miss))
        #new = list(set(new))
        return changed





