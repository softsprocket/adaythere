
from app.lib.components.element import Elements

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

class SelectDayModal (Modal):

    def __init__ (self):

        super (SelectDayModal, self).__init__ ("selectDayModalContent.html")
        modalHeader = Elements ()
        modalHeader.append_to_element ("""
            <h3>Select Day</h3>
        """)
        self.add_header_content (modalHeader)
        modalBody = Elements ()
        modalBody.append_to_element ("""

        """)
        self.add_body_content (modalBody)
        modalFooter = Elements ()
        modalFooter.append_to_element ("""
            <button class="btn btn-primary" ng-click="selectday_modal_ok ()">OK</button>
            <button class="btn btn-warning" ng-click="selectday_modal_cancel ()">Cancel</button>""")
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
            <input type="button" value="Load Files From Disk" ng-click="hide_pic_loader=!hide_pic_loader" class="btn btn-primary"/>
            <div ng-init="hide_pic_loader=true" collapse="hide_pic_loader">
             <legend>Pic Loader</legend>
             <div id="pic_loader_div" class= "well well-lg">
                <input type="file" ng-model-instant id="photo_file_uploader" multiple onchange="angular.element (this).scope ().file_selection (this)"  accept="image/*" class="btn btn-warning" />
             </div>
            </div>
            </fieldset>
             <legend>Saved Pics</legend>
             <fieldset class="fieldset_box">
             <div id="stored_pics_div" ng-repeat="stored_pic in photo_storage.available_files">
                <ul>
                    <li>
                        <a href ng-click="display_pic (stored_pic.title)">{{ stored_pic.title }}</a>
                        <input type="checkbox" ng-model="confirmed" ng-change="stored_pics_selection_changed (stored_pic, confirmed)" 
                            id="stored_pics_selection_checkbox"> <div ng-show="stored_pic.used_by.length!=0">Used by: {{ stored_pic.used_by }}</div>
                        <div collapse="is_collapsed (stored_pic.title)">
                                <div class="well well-lg" id="{{ stored_pic.title }}"></div> 
                        </div>
                    </li>
                </ul>
             </div>
             </fieldset>
             
        """)
        self.add_body_content (modalBody)
               
        modalFooter = Elements ()
        modalFooter.append_to_element ("""
            <button class="btn btn-primary" ng-click="addphotos_modal_delete ()">Delete Selected</button>
            <button class="btn btn-primary" ng-click="addphotos_modal_add_to_day ()">Add Selected To Day</button>
            <button class="btn btn-warning" ng-click="addphotos_modal_close ()">Close</button>
            <div class="fieldset_box">
                <image id="pic_loader_hidden_image" style="display:none"></image>
                <p> {{ photo_storage.count }} photos stored<br/> {{ photo_storage.total_allowed }} allowed</p>
            </div>
        """)

        self.add_footer_content (modalFooter)

