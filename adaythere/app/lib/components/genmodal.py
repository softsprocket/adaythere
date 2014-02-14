
from app.lib.components.element import Elements

class Modal(object):

    def __init__(self, template_id):
        self.elements = Elements()
        self.elements.open_element("script", {"type":"text/ng-template", "id":template_id});
        
        self.header_contents = Elements()
        self.header_contents.open_element("div", {"class":"modal-header"})

        self.body_contents = Elements()
        self.body_contents.open_element("div", {"class":"modal-body"})

        self.footer_contents = Elements()
        self.footer_contents.open_element("div", {"class":"modal-footer"})
        

    def add_header_content(self, elements):
        self.header_contents.append_to_element(elements.get())

    def add_body_content(self, elements):
        self.body_contents.append_to_element(elements.get())

    def add_footer_content(self, elements):
        self.footer_contents.append_to_element(elements.get())


    def get(self):
        self.header_contents.close_element("div")
        self.body_contents.close_element("div")
        self.footer_contents.close_element("div")

        self.elements.append_to_element(self.header_contents.get())
        self.elements.append_to_element(self.body_contents.get())
        self.elements.append_to_element(self.footer_contents.get())

        self.elements.close_element("script")

        return self.elements.get()


class ProfileModal(Modal):

    def __init__(self):

        super(ProfileModal, self).__init__("profileModalContent.html")
        profileModalHeader = Elements()
        profileModalHeader.append_to_element("<h3>User Profile</h3>")
        self.add_header_content(profileModalHeader)
        profileModalBody = Elements()
        profileModalBody.append_to_element("""
            <ul>
                <li ng-repeat="(key, value) in profile_body_content">{{ key }} : {{ value }}</li>
            </ul>
        """)
        self.add_body_content(profileModalBody)
        profileModalFooter = Elements()
        profileModalFooter.append_to_element("""
            <button class="btn btn-primary" ng-click="ok()">OK</button>
            <button class="btn btn-warning" ng-click="cancel()">Cancel</button>""")
        self.add_footer_content(profileModalFooter)

class MarkerModal(Modal):

    def __init__(self):

        super(MarkerModal, self).__init__("markerModalContent.html")
        markerModalHeader = Elements()
        markerModalHeader.append_to_element("<h3>{{ marker_title }}</h3>")
        self.add_header_content(markerModalHeader)
        markerModalBody = Elements()
        markerModalBody.append_to_element("""
            <div>{{ types }}</div>
            <div>{{ vicinity }}</div>
        """)
        self.add_body_content(markerModalBody)
        markerModalFooter = Elements()
        markerModalFooter.append_to_element("""
            <button class="btn btn-primary" ng-click="ok()">OK</button>
            <button class="btn btn-warning" ng-click="cancel()">Cancel</button>""")
        self.add_footer_content(markerModalFooter)


