class UniElement():

    def __init__(self, browser, elem=None):
        self.browser = browser
        self.elem = elem
        trig = True
        for browser_elem in self.browser.all_elems:
            if browser_elem.elem.xpath == self.elem.xpath:
                trig = False
                break
        if trig:
            self.browser.all_elems.append(self)

    def update(self):
        #try:
        self.elem = self.browser.find_element_by_xpath(self.elem.xpath)
        #except:
        #    self.elem = None