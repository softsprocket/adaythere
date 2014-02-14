"""
    represents a top level html 5 document
"""

from app.lib.components.element import Elements

class Html5Document:

    def __init__(self, title, attributes=None):
        """
            initializes the html doc string
            title - the doc title
            attributes - a dict to be turned into the attributes
            if a value is set to None then the attribute will be empty, however
            an empty string will be preserved as such
        """

        attribute_str = ""

        if attributes is not None:
            for k, v in attributes.iteritems():
                if v is not None:
                    attribute_str += ' {0}="{1}"'.format(k, v)
                else:
                    attribute_str += ' {0}'.format(k)

        self.html = """
            <!DOCTYPE html>
            <html {0}>
        """.format(attribute_str)

        self.head = """
                <head>
                    <title>{0}</title>
        """.format(title)

        self.elements = Elements()
        self.scripts = ""
        self.body = None


    def add_meta_tags(self, tags):
        """
            tags - a list of dicts to be turned into meta tags
            i.e. [{"name":"description", "content":"Helo World"}, {"charset":"UTF-8"}]
            if a value is set to None then the attribute will be empty, however
            an empty string will be preserved as such
        """

        for tag in tags:
            self.head += """
                    <meta """

            for k, v in tag.iteritems():
                if v is not None:
                    self.head += ' {0}="{1}"'.format(k, v)
                else :
                    self.head += ' {0}'.format(k)
            self.head += ">"

        return self


    def add_links(self, links):
        """
            a list of dicts to be turned into link tags
            i.e. [{"rel":"stylesheet", "href":"css/main.css"}, {"rel":"stylesheet", "type":"text/css", "href":"theme.css"}]
            if a value is set to None then the attribute will be empty, however
            an empty string will be preserved as such
        """

        for link in links:
            self.head += """
                    <link """

            for k, v in link.iteritems():
                if v is not None:
                    self.head += ' {0}="{1}"'.format(k, v)
                else :
                    self.head += ' {0}'.format(k)
            self.head += ">"

        return self


    def add_script_tags_for_head(self, scripts):
        """
            a list of dicts to be turned into script tags
            i.e. [{"src":"js/vendor/modernizr-2.7.1.min.js"}]
            if a value is set to None then the attribute will be empty, however
            an empty string will be preserved as such
        """

        for script in scripts:
            self.head += """
                    <script """

            for k, v in script.iteritems():
                if v is not None:
                    self.head += ' {0}="{1}"'.format(k, v)
                else :
                    self.head += ' {0}'.format(k)
            self.head += "></script>"

        return self


    def add_script_tags_for_body(self, scripts):
        """
            a list of dicts to be turned into script tags
            i.e. [{"src":"js/vendor/modernizr-2.7.1.min.js"}]
            if a value is set to None then the attribute will be empty, however
            an empty string will be preserved as such
        """
        self.scripts = ""

        for script in scripts:
            self.scripts += """
                    <script """

            for k, v in script.iteritems():
                if v is not None:
                    self.scripts += ' {0}="{1}"'.format(k, v)
                else :
                    self.scripts += ' {0}'.format(k)
            self.scripts += "></script>"

        return self


    def add_attributes_to_body(self, attributes):
        """
            attribute - a dict of attributes to be added to the body tag
        """

        attribute_str = ""

        if attributes is not None:
            for k, v in attributes.iteritems():
                if v is not None:
                    attribute_str += ' {0}="{1}"'.format(k, v)
                else :
                    attribute_str += ' {0}'.format(k)

        self.body = """
            <body{0}>""".format(attribute_str)


    def open_element(self, tag, attributes=None, text=""):

        self.elements.open_element(tag, attributes, text)
        return self

    def append_to_element(self, text):

        self.elements.append_to_element(text)
        return self


    def close_element(self, tag):

        self.elements.close_element(tag)
        return self


    def __shiv(self):

        self.head += """
                <!--[if lt IE 9]>
                    <script src="js/html5shiv.js"></script>
                <![endif]-->
        """


    def get(self):
        """
            returns the html document
        """

        self.__shiv()

        if self.body is None:
            self.body = """
            <body>
            """

        self.html += self.head
        self.html += """
            </head>
        """
        self.html += self.body
        self.html += self.elements.get()
        self.html += self.scripts
        self.html += """
            </body>
        """
        self.html += """
        </html>
        """

        return self.html

