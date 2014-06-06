from app.lib.components.form import BootstrapForm


class DaySearch (BootstrapForm):

    def __init__(self):
        super (DaySearch, self).__init__()

        self.add_select (False, {
            "multiple": None,
            "ng-multiple": "true",
            "ng-model": "daysearch_selected_keywords",
            "ng-options": "keyword for keyword in daysearch_keywords"
        })

        self.add_input_element ("daysearch_locality_input", "Locality:", {
            "ng-model": "daysearch_locality"
        })

        self.add_input_element ("daysearch_words_input", "Words:", {
            "ng-model": "daysearch_words"
        })

        self.add_input_element ("daysearch_all_words_checkbox", "All words:", {
            "type": "checkbox",
            "ng-model": "daysearch_all_words"
        })

        self.add_button ("Search", {
            "type": "button",
            "ng-click": "executeSearch()"
        })

    def get (self):

        return super (DaySearch, self).get ()

