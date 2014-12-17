from app.lib.components.element import Elements

class SendAdvertizeMail (Elements):

    def __init__(self):
        super (SendAdvertizeMail, self).__init__()


        self.open_element ("form", {"class": "simple-form"})
        self.open_element ("fieldset", {"class": "fieldset_box fieldset_send_ad_mail"})
        self.append_to_element ("<legend>Request Advertizing Information</legend>")

        self.append_to_element ("""
            <p><label class="send_ad_mail_label" for="locality_autocomplete_input">Locality:</label>
            <input id="locality_autocomplete_input" type="text" placeholder="Enter a locality" autocomplete="off" ng-model="send_ad_mail.full_locality" class="send_ad_mail_input"></input>  
        """)

        self.append_to_element ("""
            <p><label class="send_ad_mail_label" for="send_ad_mail_words_input">Search terms:</label>
            <input id="send_ad_mail_words_input" type="text" placeholder="Enter search words" ng-model="send_ad_mail.words" class="send_ad_mail_input"></input>
        """)

        self.append_to_element ("""
            <p><label class="send_ad_mail_label" for="send_ad_mail_rating">Minimum rating:</label>
            <rating id="send_ad_mail_rating" value="send_ad_mail.rating" max="send_ad_mail.max"></rating>
        """)

        self.append_to_element ("""
            <p><label class="send_ad_mail_label" for="send_ad_mail_all_words_radio">All words:</label>
            <input id="send_ad_mail_all_words_radio" type="radio" ng-model="send_ad_mail.all_words" value="all"></input>
            <p><label class="send_ad_mail_label" for="send_ad_mail_any_words_radio">Any words:</label>
            <input id="send_ad_mail_any_words_radio" type="radio" ng-model="send_ad_mail.all_words" value="any"></input>
        """)

        self.append_to_element ("""
            <p><label class="send_ad_mail_label">Keywords:</label>
            <select multiple ng-model="send_ad_mail.selected_keywords" ng-options="keyword for keyword in send_ad_mail.keywords">
                <option value="">--Choose keywords--</option>
            </select>
        """)

        self.append_to_element ("""
            <p>
            <button ng-click="send()">Send</button>
            <button ng-click="clear()" style="float:right;">Clear</button>
        """)

        self.close_element ("fieldset")
        self.close_element ("form")



    def get (self):

        return super (SendAdvertizeMail, self).get ()

