class UniElement():

    def __init__(self, browser, elem=None):
        self.browser = browser
        self.elem = elem
        self.browser.all_elems.append(self)

    def update(self):
        try:
            self.elem = self.browser.find_elements_by_xpath(self.elem.xpath)[0]
        except:
            self.elem = None