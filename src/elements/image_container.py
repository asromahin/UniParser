from src.elements.element import UniElement

class UniImageContainer(UniElement):
    def __init__(self, browser, elem=None):
        super(UniImageContainer, self).__init__(browser, elem)

        self.href = self.get_href()

    def get_href(self):
        res = self.elem.find_elements_by_attrs(attrs={'src': None}, is_sim=False)
        if res:
            return res[0]
        else:
            return []