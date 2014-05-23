from app.lib.components.element import Elements

class DayDisplay (Elements):
        
    def __init__ (self, ani_processed):
        super (DayDisplay, self).__init__ ()
        
        if (ani_processed):
            self.open_element ("div", { "class": "day-wrapper ani-processed", "style": " " })
        else:
            self.open_element ("div", { "class": "day-wrapper" })

        self.open_element ("div", { "class": "day" })


    def get (self):

        self.close_element ("div")
        self.close_element ("div")

        return super (DayDisplay, self).get ()


class DayPhotoDisplay (Elements):

    def __init__ (self, bgimage, image):
        super (DayPhotoDisplay, self).__init__ ()

        self.open_element ("div", { "class": "photo-wrapper" })
        bg = "background-image: url({0});".format (bgimage)
        self.open_element ("div", { "class": "photo", "style": bg })
        self.open_element ("img", { "alt": "", "src": image, "style": "display: none;" })
        self.close_element ("img")
        self.append_to_element ("""
            <div class="overlay">
                <span class="fui-eye"> </span>
            </div>
        """)


    def get (self):
        self.close_element ("div")
        self.close_element ("div")
        return super (DayPhotoDisplay, self).get ()


class DayInfoDisplay (Elements):

    def __init__ (self, title, text):
        super (DayInfoDisplay, self).__init__ ()

        self.open_element ("div", { "class": "info" })
        self.open_element ("div", { "class": "name" })
        self.append_to_element (title)
        self.close_element ("div")
        self.append_to_element (text)

   
    def get (self):
        self.close_element ("div")
        return super (DayInfoDisplay, self).get ()


