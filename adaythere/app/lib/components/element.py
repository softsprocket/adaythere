
class Elements (object):

    def __init__(self):
        self.elements = ""

    def open_element (self, tag, attributes=None, text=""):

        attribute_str = ""

        if attributes is not None:
            for k, v in attributes.iteritems ():
                if v is not None:
                    attribute_str += ' {0}="{1}"'.format (k, v)
                else :
                    attribute_str += ' {0}'.format (k)

        self.elements += """<{0}{1}>{2}""".format (tag, attribute_str, text)

        return self

    
    def append_to_element (self, text):
        self.elements += text

        return self


    def close_element (self, tag):

        self.elements += "</{0}>".format (tag)

        return self

    def get (self):

        return self.elements

