from src.utils.utils import filter_string

class UniNode():
    def __init__(self, soup_elem, parent_xpath='', parent=None, index=None):

        self.soup_elem = soup_elem
        self.tag = self.soup_elem.name
        self.attrs = self.soup_elem.attrs
        self.text = filter_string(self.soup_elem.getText())

        self.parent_xpath = parent_xpath

        self.parent = parent
        self.children = []
        self.children_xpath_node = {}

        self.is_changed = False

        self.index = index

        self.xpath_node = self.tag

        if self.index:
            self.xpath_node += f'[{self.index}]'

        if parent:
            self.xpath = '/'.join([parent_xpath, self.xpath_node])
        else:
            self.xpath = parent_xpath

        self.__find_children()

        self.refs = self.get_refs(is_recurse=False)

        self.data = {
            'tag': self.tag,
            'attrs': self.attrs,
            'xpath': self.xpath,
            'len_children': len(self.children),
            'text': self.text,
            'refs': self.refs,
        }

    def copy(self):
        return UniNode(soup_elem=self.soup_elem, parent_xpath=self.parent_xpath, parent=self.parent, index=self.index)

    def __set_child(self, soup_elem, index=None):
        node = UniNode(soup_elem, parent_xpath=self.xpath, parent=self, index=index)
        self.children.append(node)
        self.children_xpath_node[node.xpath_node] = node

    def __find_children(self):
        children = self.soup_elem.findChildren(recursive=False)
        tag_dict = {}
        for child in children:
            if child.name in tag_dict.keys():
                tag_dict[child.name].append(child)
            else:
                tag_dict[child.name] = [child]
        for key in tag_dict.keys():
            tag_children = tag_dict[key]
            for i, child in enumerate(tag_children):
                if len(tag_children) > 1:
                    self.__set_child(child, index=i+1)
                else:
                    self.__set_child(child, index=None)

    def __find_elements_by(self, by_key, func_is, func_value=None, value_key=None, is_sim=True, is_recurse=True, is_children=True):
        if not func_value:
            func_value = self.__get_pass
        res = []
        if is_children:
            for child in self.children:
                if func_is(by_key=by_key, child=child, is_sim=is_sim):
                    value = func_value(child, value_key)
                    res.append(value)
                if is_recurse:
                    res.extend(child.__find_elements_by(by_key=by_key, func_is=func_is, func_value=func_value,
                                                        value_key=value_key, is_sim=is_sim, is_recurse=True, is_children=is_children))
        else:
            if self.parent:
                if func_is(by_key=by_key, child=self.parent, is_sim=is_sim):
                    value = func_value(self.parent, value_key)
                    res.append(value)
                if is_recurse:
                    res.extend(self.parent.__find_elements_by(by_key=by_key, func_is=func_is, func_value=func_value,
                                                        value_key=value_key, is_sim=is_sim, is_recurse=True, is_children=is_children))
        return res

    def __find_element_by(self, by_key, func_is, func_value=None, value_key=None, is_sim=True, is_recurse=True, is_children=True):
        if not func_value:
            func_value = self.__get_pass
        if is_children:
            for child in self.children:
                if func_is(by_key=by_key, child=child, is_sim=is_sim):
                    value = func_value(child=child, key=value_key)
                    return value
                if is_recurse:
                    res = child.__find_element_by(by_key=by_key, func_is=func_is, func_value=func_value,
                                                   value_key=value_key, is_sim=is_sim, is_recurse=True, is_children=is_children)
                    if res:
                        return res
        else:
            if self.parent:
                if func_is(by_key=by_key, child=self.parent, is_sim=is_sim):
                    value = func_value(child=self.parent, key=value_key)
                    return value
                if is_recurse:
                    res = self.parent.__find_element_by(by_key=by_key, func_is=func_is, func_value=func_value,
                                                   value_key=value_key, is_sim=is_sim, is_recurse=True, is_children=is_children)
                    if res:
                        return res
        return None

    def __by_pass(self, child, by_key, is_sim=False):
        return True

    def __by_xpath(self, child, by_key, is_sim=False):
        if is_sim:
            return by_key == child.xpath
        else:
            return by_key in child.xpath

    def __by_elem(self, child, by_key, is_sim=False):
        return by_key == child

    def __by_changed(self, child, by_key=None, is_sim=False):
        return child.is_changed

    def __by_tag_name(self, child, by_key=None, is_sim=False):
        if is_sim:
            return by_key == child.tag
        else:
            return by_key in child.tag

    def __by_attrs(self, by_key, child, is_sim=True):
        if not child.attrs.keys():
            if by_key:
                return False
            else:
                return True
        for attr_key in by_key.keys():
            for child_attr_key in child.attrs.keys():
                if is_sim:
                    if attr_key == child_attr_key:
                        if by_key[attr_key]:
                            if type(child.attrs[child_attr_key]) == type([]):
                                for key in child.attrs[child_attr_key]:
                                    if key:
                                        if key == by_key[attr_key]:
                                            return True
                            else:
                                if child.attrs[child_attr_key] == by_key[attr_key]:
                                    return True
                        else:
                            return True
                else:
                    if attr_key in child_attr_key:
                        if by_key[attr_key]:
                            if type(child.attrs[child_attr_key]) == type([]):
                                for key in child.attrs[child_attr_key]:
                                    if key:
                                        if by_key[attr_key] in key:
                                            #print(key, by_key[attr_key])
                                            return True
                            else:
                                if child.attrs[child_attr_key] in by_key[attr_key]:

                                    return True
                        else:
                            return True
        return False

    def find_elements_by_tag_name(self, tag, is_recurse=True, is_sim=False, is_children=True):
        return self.__find_elements_by(by_key=tag, func_is=self.__by_tag_name, is_recurse=is_recurse, is_sim=is_sim, is_children=is_children)

    def find_elements_by_changed(self, is_recurse=True, is_sim=False, is_children=True):
        return self.__find_elements_by(by_key=None, func_is=self.__by_changed, is_recurse=is_recurse, is_sim=is_sim, is_children=is_children)

    def find_elements_by_attrs(self, attrs={}, is_recurse=True, is_sim=True, is_children=True):
        return self.__find_elements_by(by_key=attrs, func_is=self.__by_attrs, is_recurse=is_recurse, is_sim=is_sim, is_children=is_children)

    def find_element(self, elem, is_recurse=True, is_sim=True, is_children=True):
        return self.__find_element_by(by_key=elem, func_is=self.__by_elem, is_recurse=is_recurse, is_sim=is_sim,
                                       is_children=is_children)

    """def find_elements_by_xpath(self, xpath, is_recurse=True, is_sim=False, is_children=True):
        return self.__find_elements_by(by_key=xpath, func_is=self.__by_xpath, is_recurse=is_recurse, is_sim=is_sim, is_children=is_children)

    def find_element_by_xpath(self, xpath, is_recurse=True, is_sim=False, is_children=True):
        return self.__find_element_by(by_key=xpath, func_is=self.__by_xpath, is_recurse=is_recurse, is_sim=is_sim, is_children=is_children)"""

    def find_element_by_xpath(self, xpath, is_recurse=True, is_sim=False, is_children=True):
        if xpath[0] == '/':
            xpath = xpath[1:]
        xpath_nodes = xpath.split('/')
        if xpath_nodes[0] in self.children_xpath_node:
            if len(xpath_nodes) > 1:
                return self.children_xpath_node[xpath_nodes[0]].find_element_by_xpath('/'.join(xpath_nodes[1:]), is_recurse=True, is_sim=False, is_children=True)
            else:
                return self.children_xpath_node[xpath_nodes[0]]
        else:
            return None

    def __get_pass(self, child, key=None):
        return child

    def __get_attrs(self, child, key=None):
        if key:
            return child.attrs[key]
        else:
            return child.attrs

    def __get_data(self, child, key=None):
        if key:
            return child.data[key]
        else:
            return child.data

    def get_children(self, is_recurse=False):
        return self.__find_elements_by(by_key=None, func_is=self.__by_pass, func_value=None, value_key=None,
                                       is_recurse=is_recurse, is_sim=True)

    def get_children_attrs(self, attr_key, value_key, is_recurse=True, is_sim=True):
        return self.__find_elements_by(by_key=attr_key, func_is=self.__by_attrs, func_value=self.__get_attrs, value_key=value_key,
                                       is_recurse=is_recurse, is_sim=is_sim)

    def get_selenium_element(self, wd):
        return wd.find_element_by_xpath(self.xpath)

    def __eq__(self, other):
        if self.data != other.data:
            return False
        else:
            return True

    def __hash__(self):
        return hash((self.xpath))

    def get_difference(self, other_node, is_recurse=True):
        changed_res = []
        miss_res = []
        new_res = []
        children = self.get_children(is_recurse=True)
        other_children = other_node.get_children(is_recurse=True)
        for child in children:
            node = other_node.find_element_by_xpath(child.xpath)
            if node:
                if child != node:
                    changed_res.append(child)
                    child.is_changed = True
            else:
                miss_res.append(child)

        for child in other_children:
            node = self.find_element_by_xpath(child.xpath)
            if not node:
                new_res.append(child)

        return changed_res, miss_res, new_res

    def get_refs(self, is_recurse=False):
        res = {}
        for attr_key in self.attrs.keys():
            if 'ref' in attr_key or 'src' in attr_key:
                res[attr_key] = self.attrs[attr_key]
        if is_recurse:
            for child in self.children:
                res.update(child.get_refs(is_recurse=is_recurse))
        return res
