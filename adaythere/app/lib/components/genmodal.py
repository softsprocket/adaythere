
from app.lib.components.element import Elements
from app.adaythere import ADayThere

class Modal (object):

    def __init__ (self, template_id):
        self.elements = Elements ()
        self.elements.open_element ("script", {"type":"text/ng-template", "id":template_id});
        
        self.header_contents = Elements ()
        self.header_contents.open_element ("div", {"class":"modal-header"})

        self.body_contents = Elements ()
        self.body_contents.open_element ("div", {"class":"modal-body"})

        self.footer_contents = Elements ()
        self.footer_contents.open_element ("div", {"class":"modal-footer"})
        

    def add_header_content (self, elements):
        self.header_contents.append_to_element (elements.get ())

    def add_body_content (self, elements):
        self.body_contents.append_to_element (elements.get ())

    def add_footer_content (self, elements):
        self.footer_contents.append_to_element (elements.get ())


    def get (self):
        self.header_contents.close_element ("div")
        self.body_contents.close_element ("div")
        self.footer_contents.close_element ("div")

        self.elements.append_to_element (self.header_contents.get ())
        self.elements.append_to_element (self.body_contents.get ())
        self.elements.append_to_element (self.footer_contents.get ())

        self.elements.close_element ("script")

        return self.elements.get ()


class ProfileModal (Modal):

    def __init__ (self):

        super (ProfileModal, self).__init__ ("profileModalContent.html")
        profileModalHeader = Elements ()
        profileModalHeader.append_to_element ("<h3>User Profile</h3>")
        self.add_header_content (profileModalHeader)
        profileModalBody = Elements ()
        profileModalBody.append_to_element ("""
            <ul>
                <li ng-repeat="(key, value) in profile_body_content">{{ key }} : {{ value }}</li>
            </ul>
        """)
        self.add_body_content (profileModalBody)
        profileModalFooter = Elements ()
        profileModalFooter.append_to_element ("""
            <button class="btn btn-primary" ng-click="ok ()">OK</button>
            <button class="btn btn-warning" ng-click="cancel ()">Cancel</button>""")
        self.add_footer_content (profileModalFooter)

class MarkerModal (Modal):

    def __init__ (self):

        super (MarkerModal, self).__init__ ("markerModalContent.html")
        markerModalHeader = Elements ()
        markerModalHeader.append_to_element ("""
            <h1>Marker</h1>
        """)
        self.add_header_content (markerModalHeader)
        markerModalBody = Elements ()
        markerModalBody.append_to_element ("""
            <label for="marker_modal_title">Name</label> 
            <input id="marker_modal_title" class="form-control" type='text' ng-disabled="!marker_content.is_editable" ng-model='marker_content.name'></input>
            <label for="marker_modal_address">Address</label>
            <input id="marker_modal_address" class="form-control" type='text' ng-disabled="!marker_content.is_editable" ng-model='marker_content.vicinity'></input>
            <label for="marker_modal_own_comments">Comments</label>
            <textarea id="marker_modal_own_comments"  class="form-control" ng-disabled="!marker_content.is_editable" ng-model='marker_content.comment'></textarea>
        """)
        self.add_body_content (markerModalBody)
        markerModalFooter = Elements ()
        markerModalFooter.append_to_element ("""
            <button ng-show="show_add_button" class="btn btn-primary" ng-click="marker_modal_add_to_day (marker_content)">Add To Day</button>
            <button class="btn btn-primary" ng-click="marker_modal_ok ()">OK</button>
            <button class="btn btn-warning" ng-click="marker_modal_cancel ()">Cancel</button>""")
        self.add_footer_content (markerModalFooter)

class BecomeAContributorModal (Modal):

    def __init__ (self):

        super (BecomeAContributorModal, self).__init__ ("becomeAContributorModalContent.html")

        logged_in, db_user = ADayThere.logged_in_user ()
        body_html = ""
        if logged_in:
            suggest_change = ""
            if db_user.name == db_user.email:
                suggest_change = """*Please, change your user name to something other then your email address to avoid spam.
                                Only alphanumeric characters and the underscore (_) are accepted."""

            if not logged_in:
                body_html += "You must be logged in through Google before becoming a contributor"
            else:
                body_html += """
                    <div>Thanks for choosing to become a contributor to the community. We ask that you don't use language that would make
                        anyone's Grandmother blush. Be repectful of others who use "A Day There". By clicking the OK button you agree
                        to allow "A Day There" to use the material you contribute and to abide by the rules.<br/><br/>
                        Thank You!<br/>
                    </div>
                    <div id="contributor_name_choice" style="color:red;">{0}</div>
                    <label for="contribute_google_nickname">Name:</label> 
                    <input data-warning-id="contributor_name_choice" id="contribute_google_nickname" class="form-control" type='text' contributor-user-name value="{1}"></input>
                    <input id="contribute_gotto_tools" type="checkbox">Go to create tools</input>
                """.format (suggest_change, db_user.name)

        modalHeader = Elements ()
        modalHeader.append_to_element ("""
            <h3>Become A Contributor</h3>
        """)
        self.add_header_content (modalHeader)
        modalBody = Elements ()
        modalBody.append_to_element (body_html)
        self.add_body_content (modalBody)
        modalFooter = Elements ()
        modalFooter.append_to_element ("""
            <button class="btn btn-primary" ng-click="contribute_modal_ok ()">OK</button>
            <button class="btn btn-warning" ng-click="contribute_modal_cancel ()">Cancel</button>""")
        self.add_footer_content (modalFooter)

class AdminProfileModal (Modal):

    def __init__ (self):

        super (AdminProfileModal, self).__init__ ("adminProfileModalContent.html")
        modalHeader = Elements ()
        modalHeader.append_to_element ("""
            <h3>Profiles</h3>
        """)
        self.add_header_content (modalHeader)
        modalBody = Elements ()
        modalBody.append_to_element ("""
        <label for="name">Name: </label>
        <input id="name" class="form-control" type='text' ng-model='search_on.name'></input>
        <label for="email">Email: </label>
        <input id="email" class="form-control" type='text' ng-model='search_on.email'></input>        
        <label for="userid">UserId: </label>
        <input id="userid" class="form-control" type='text' ng-model='search_on.userid'></input>
        """)
        self.add_body_content (modalBody)
        modalFooter = Elements ()
        modalFooter.append_to_element ("""
        <button class="btn btn-primary" ng-click="adminprofile_modal_ok ()">Search</button>
        <button class="btn btn-warning" ng-click="adminprofile_modal_cancel ()">Close</button>
        <div>----------------------------------------------------------------</div>
        <div ng-repeat="user in received_profile_data.users">
            <ul>
                <li ng-repeat="(key, value) in user">{{ key }} : {{ value }}</li>
            </ul>
            <button ng-disabled="!user.banned" ng-click="adminprofile_modal_ban (user, false)">Unban</button>
            <button ng-disabled="user.banned" ng-click="adminprofile_modal_ban (user, true)">Ban</button>
            <div>----------------------------------------------------------------</div>
        </div>
        <div ng-if="received_profile_data.more">More</div>
        """)

        self.add_footer_content (modalFooter)


class AddPhotosModal (Modal):

    def __init__ (self):

        super (AddPhotosModal, self).__init__ ("addPhotosModalContent.html")
        modalHeader = Elements ()
        modalHeader.append_to_element ("""
            <h3>Photos</h3>
        """)
        self.add_header_content (modalHeader)

        modalBody = Elements ()
        modalBody.append_to_element ("""
            <fieldset class="fieldset_box">
            <input type="button" value="Load Files From Disk" ng-click="open_file_selection()" class="btn btn-primary"/>
            <div collapse="false">
             <div  collapse="true" class= "well well-lg">
                <input id="open_file_selection" type="file" ng-model-instant id="photo_file_uploader" multiple onchange="angular.element (this).scope ().file_selection (this)"  accept="image/*" class="btn btn-warning" />
             </div>
             </fieldset>
             <fieldset class="fieldset_box">
             <div id="pic_loader_div">

             </div>
            </div>
            </fieldset>
        """)
        self.add_body_content (modalBody)
               
        modalFooter = Elements ()
        modalFooter.append_to_element ("""
            <button class="btn btn-primary" ng-click="remove_checked_photos ()">Remove Selected</button>
            <button class="btn btn-primary" ng-click="upload_checked_photos ()">Add Selected To Day</button>
            <button class="btn btn-warning" ng-click="addphotos_modal_close ()">Close</button>
            <div class="fieldset_box">
                <image id="pic_loader_hidden_image" style="display:none"></image>
                <p> {{ photo_storage.count }} photos stored<br/> {{ photo_storage.total_allowed }} allowed</p>
            </div>
        """)

        self.add_footer_content (modalFooter)

class HelpModal (Modal):

    def __init__ (self):

        super (HelpModal, self).__init__("helpModalContent.html")
        modalHeader = Elements ()
        modalHeader.append_to_element ("""
            <h3>Help</h3>
        """)
        self.add_header_content (modalHeader)

        modalBody =Elements ()
        modalBody.append_to_element ("""
            <ol class="help_list">
                <li class="help"><a href="#searching">Searching</a></li>
                    <ol class="help_list_inner">
                        <li class="help"><a href="#search_locality">Locality Field</a></li>
                        <li class="help"><a href="#search_terms">Search Terms</a></li>
                    </ol>
            </ol>
            <h3><a id="searching">Searching</a></h3>
            <p>The "Day Search" form is available whether you log in or not. The simplest search is to click the "Random Days"
                button. This will display a list of random results. Click on a title to see the day. You can return to the search
                by clicking the "Search Again" button or using the menu item, accessed by clicking your user name in the menu bar.
            </p>
            <h4><a id="search_locality">Locality</a></h4>
            <p>Enter the region you wish to search in the "Locality" field. It has autocomplete ability and will attempt to help 
                you find the region you're looking for.
            </p>
            <h4><a id="search_terms">Search Terms</a></h4>
            <p>The "Search Terms" field allows you to narrow your search based on words potentially found in the description or title
                of a day.
            </p>
        """)

        self.add_body_content (modalBody)
               
        modalFooter = Elements ()
        modalFooter.append_to_element ("""
            <button class="btn btn-warning" ng-click="close ()">Close</button>
        """)

        self.add_footer_content (modalFooter)

