from app.lib.components.element import Elements

class FormGroup (Element):

    def __init__(self):

        super(FormGroup, self).__init__()
        self.open_element("div", { "class":"form-group" }


    def append_input_element(label, attributes):
        self.append_to_element("<label>{0}</label>".format(label))
        self.open_element("input", attributes)
        self.close_element("input");


    def get(self):
        self.close_element("div")
        return super(FormGroup, self).get();
  
