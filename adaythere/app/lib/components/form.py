
from app.lib.components.element import Elements

class BootstrapForm (Elements):

    def __init__ (self):
        super (BootstrapForm, self).__init__()

        self.open_element ("form", { "role": "form" })


    def add_input_element (self, identifier, label, attrs):
        self.open_element ("div", { "class": "form-group" })
        
        self.open_element ("label", { "for": identifier })
        self.append_to_element (label)
        self.close_element ("label")

        attr = attrs
        attr["id"] = identifier
        attr["class"] = "form-group"

        self.open_element ("input", attr)

        self.close_element ("div")

    def add_button (self, text, attr):
        self.open_element ("button", attr)
        self.append_to_element (text)
        self.close_element ("button")
    
    def add_select (self, nullable, attrs):
        if nullable:
            self.open_element ("span", { "class": "nullable" })

        self.open_element ("select", attrs)
        self.close_element ("select")

        if nullable:
            self.close_element ("span")


    def get (self):

        self.close_element ("form")

        return super (BootstrapForm, self).get ()



