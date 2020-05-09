import pandas as pd

class UniBehaviour():

    def __init__(self, browser):
        self.browser = browser
        self.child = None
        self.parent = None

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

    def get_data(self, result={}):
        pass


class UniBehaviourStart(UniBehaviour):

    def __init__(self, browser):
        super(UniBehaviourStart, self).__init__(browser=browser)

    def get_data(self, result={}):
        for table in self.browser.tables:
            result[table.elem.xpath] = pd.DataFrame(table.table_data)
        return result


class UniBehaviourMovePaginator(UniBehaviour):

    def __init__(self, browser, paginator, max_page=None):
        super(UniBehaviourMovePaginator, self).__init__(browser=browser)
        self.paginator = paginator
        self.cur_page = 0
        self.max_page = max_page

    def move(self, result={}):
        is_next = self.paginator.next()
        while is_next:
            #print(is_next, self.paginator, self.paginator.elem)
            result = self.get_data(result)
            is_next = self.paginator.next()
            self.cur_page += 1
            if self.max_page:
                if self.cur_page >= self.max_page:
                    break
        return result

    def get_data(self, result={}):
        for table in self.browser.tables:
            if table.elem.xpath in result.keys():
                result[table.elem.xpath] = pd.concat([result[table.elem.xpath], pd.DataFrame(table.table_data)])
            else:
                result[table.elem.xpath] = pd.DataFrame(table.table_data)
        return result



