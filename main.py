import sqlite3

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.button import MDRoundFlatIconButton
from pymongo import MongoClient
from kivy.metrics import *
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty, ListProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.boxlayout import BoxLayout, MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.screen import MDScreen

searchBarData = []
cluster = MongoClient("mongodb://library:pencil1234@44.199.16.91:29017/?authSource=admin")
db = cluster["lapiz"]

collection = db["lib_resource"]
results = collection.find()

for r in results:
    book = r
    searchBarData.append(book)


def _create_local_db():
    """ Start with a Local DataBase, create one if it does not exist. """

    try:
        connection = sqlite3.connect("school.db")
        cursor = connection.cursor()

        cursor.execute(""" CREATE TABLE user
            (studentId varchar   NOT NULL,
            password varchar NOT NULL,
            entries varchar,
            name varchar,
            current_class varchar,
            phone varchar,
            photo_link varchar)
         """)

        cursor.execute(""" CREATE INDEX studentId on user (studentId) """)
        cursor.execute(""" CREATE INDEX password on user (password) """)
        cursor.execute(""" CREATE INDEX name on user (name) """)
        cursor.execute(""" CREATE INDEX current_class on user (current_class) """)
        cursor.execute(""" CREATE INDEX phone on user (phone) """)
        cursor.execute(""" CREATE INDEX photo_link on user (photo_link) """)

        connection.commit()
        cursor.close()
        connection.close()
    except sqlite3.OperationalError:
        pass


# ----- Recycle view options------- #


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class CatalogData(RecycleDataViewBehavior, BoxLayout):
    """ Catalog Items from search """


# class SelectableButton(RecycleDataViewBehavior, GridLayout):
#
#     """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """

        self.index = index
        return super(CatalogData, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add Selection on touch down """
        if super(CatalogData, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """


# ----- Recycle view options end------- #

class CatalogSearchScreen(ThemableBehavior, MDScreen):
    """ Dashboard class for items Catalog search """

    def __init__(self, **kwargs):
        super(CatalogSearchScreen, self).__init__(**kwargs)


class CatalogSearchBoxScreen(BoxLayout):
    """

    Displays catalog search items.

    """

    def __init__(self, **kwargs):
        super(CatalogSearchBoxScreen, self).__init__(**kwargs)

    def set_items_list(self, text="", search=False):
        """ Builds a list of items for the screen """

        def add_item(item_name):
            self.ids.search_results_list.data.append(
                {
                    "viewclass": "CatalogData",
                    "d_auth_name": item_name.get('author_code'),
                    "d_book_title": item_name.get('resource_desc'),
                }
            )

        self.ids.search_results_list.data = []
        for item_name in searchBarData:
            if search:
                if text.lower() in item_name.get('resource_desc').lower():
                    add_item(item_name)
            else:
                add_item(item_name)


class LibraryDashboardScreen(ThemableBehavior, MDScreen):
    """

    Displays catalog search items.

    """

    def __init__(self, **kwargs):
        super(LibraryDashboardScreen, self).__init__(**kwargs)


class LibraryDashboardBoxScreen(BoxLayout):
    """ show borrowed, hold request and  ready to pickup options"""

    lib_search_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(LibraryDashboardBoxScreen, self).__init__(**kwargs)

    def search_cloud_data(self):
        catalog_search_entry = self.ids.lib_search_input.text


class LogInScreen(ThemableBehavior, MDScreen):
    password_entered = ObjectProperty()
    student_id = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def switch_to_dashboard_screen(self):
        self.parent.current = 'LibraryDashboardScreen'

    def get_user_password(self):
        """ implement MongoDB connection to users that already has access their account"""

        password_entry = self.password_entered
        student_id_ent = self.student_id
        # self.switch_to_dashboard_screen()

        cluster = MongoClient("mongodb://library:pencil1234@44.199.16.91:29017/?authSource=admin")
        db = cluster["lapiz"]

        stud_results = db.student.find({'_id': student_id_ent.text})

        for r in stud_results:
            F_name = r.get('first_name')
            S_name = r.get('last_name')
            person_name = F_name + ' ' + S_name
            person_grade = r.get('current_class')
            person_id = r.get('_id')
            person_phone = r.get('phone')
            person_password = r.get('password')
            profile_image_link = r.get('photo_lnk')

            if person_password != password_entry.text or len(person_password) == 0:
                wrong_password_dialog = MDDialog(text="Wrong Username/Password")
                wrong_password_dialog.radius = [20, 7, 20, 7]
                wrong_password_dialog.size_hint_x = dp(0.5)
                wrong_password_dialog.open()

            elif person_id != student_id_ent.text or len(person_id) == 0:
                wrong_password_dialog = MDDialog(text="Wrong Username/Password")
                wrong_password_dialog.radius = [20, 7, 20, 7]
                wrong_password_dialog.size_hint_x = dp(0.5)
                wrong_password_dialog.open()

            else:

                ''' Temporary MongoDb user storage [ on_user_logIn ]'''
                name = person_name
                grade = person_grade
                stud_id = person_id
                phone = person_phone
                passwd = person_password
                photo_link = profile_image_link

                connection = sqlite3.connect("school.db")
                cursor = connection.cursor()
                data_query = "insert into user (name, current_class, studentId, phone, password, photo_link) values ('" + name + "', '" + grade + "', '" + stud_id + "', '" + phone + "', '" + passwd + "', '" + photo_link + "' )"
                cursor.execute(data_query)

                connection.commit()
                cursor.close()
                connection.close()

                ''' Temporary MongoDb user storage END'''

                self.switch_to_dashboard_screen()
                password_entry.text = ''
                student_id_ent.text = ''


class PhoneUpdateDialog(BoxLayout):
    """ Show a pop up dialog to update phone number to the database """


class PasswordUpdateDialog(BoxLayout):
    """ Show a pop up dialog to update password to the database """


class PasswordPhoneUpdateScreen(ThemableBehavior, MDScreen):
    """ Ability of users to change their passwords """

    def __init__(self, **kwargs):
        super(PasswordPhoneUpdateScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        toast('Touch to Update', duration=2.0)


class PasswordPhoneBoxUpdate(BoxLayout):
    """ Password change ability container """

    def __init__(self, **kwargs):
        super(PasswordPhoneBoxUpdate, self).__init__(**kwargs)

    def show_password_update_dialog(self):
        pop_pass_change = PasswordUpdateDialog()
        pop_pass_change.open()

    def show_phone_update_dialog(self):
        pop_phone_change = PhoneUpdateDialog()
        pop_phone_change.open()


class PasswordUpdateDialog(Popup):
    """ Show a pop up dialog to update password to the database """

    update_password = ObjectProperty()

    def __init__(self, **kwargs):
        super(PasswordUpdateDialog, self).__init__(**kwargs)

    def get_pass_update(self):
        password_update = self.update_password

        cluster = MongoClient("mongodb://library:pencil1234@44.199.16.91:29017/?authSource=admin")
        db = cluster["lapiz"]

        connection = sqlite3.connect("school.db")
        cursor = connection.cursor()
        data_query = "select * from user"
        cursor.execute(data_query)

        fetch = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        self.student_id = fetch[0]
        self.recent_password = fetch[1]
        self.recent_phone = fetch[5]

        stud_results = db.student.find({'_id': self.student_id})
        for r in stud_results:
            person_password = r.get('password')

            mycol = db["student"]

            myquery = {"password": person_password}
            newvalues = {"$set": {"password": password_update.text}}

            mycol.update_one(myquery, newvalues)


class PhoneUpdateDialog(Popup):
    """ Show a pop up dialog to update password to the database """

    update_phone = ObjectProperty()

    def __init__(self, **kwargs):
        super(PhoneUpdateDialog, self).__init__(**kwargs)

    def get_phone_update(self):
        """ method to update user phone number """

        phone_update = self.update_phone
        cluster = MongoClient("mongodb://library:pencil1234@44.199.16.91:29017/?authSource=admin")
        db = cluster["lapiz"]

        connection = sqlite3.connect("school.db")
        cursor = connection.cursor()
        data_query = "select * from user"
        cursor.execute(data_query)

        fetch = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        self.student_id = fetch[0]

        stud_results = db.student.find({'_id': self.student_id})
        for r in stud_results:
            person_phone = r.get('phone')

            mycol = db["student"]

            myquery = {"phone": person_phone}
            newvalues = {"$set": {"phone": phone_update.text}}

            mycol.update_one(myquery, newvalues)


class SchoolApp(MDApp):
    """ Main class Application """
    _name_data = 'name'
    _grade_data = 'grade'
    _student_id_data = 'id'
    _phone_data = 'phone'
    _password_data = '******'
    _profile_image = ''

    name = ObjectProperty(_name_data)
    grade = ObjectProperty(_grade_data)
    student_id = ObjectProperty(_student_id_data)
    phone = ObjectProperty(_phone_data)
    password = ObjectProperty(_password_data)
    profile_image = ObjectProperty(_profile_image)

    def get_user_profile_info(self):

        connection = sqlite3.connect("school.db")
        cursor = connection.cursor()
        data_query = "select * from user"
        cursor.execute(data_query)

        fetch = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        self.name = fetch[3]
        self.grade =  fetch[4]
        self.student_id = fetch[0]
        self.phone = fetch[5]
        self.password = fetch[1]
        self.profile_image = fetch[6]

    def __init__(self, **kwargs):
        super(SchoolApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Indigo"

    def switch_to_catalog_screen(self):
        self.root.current = 'CatalogSearchScreen'

    def switch_to_password_screen(self):
        self.root.current = 'PasswordPhoneUpdateScreen'

    def switch_to_dashboard_screen(self):
        self.root.current = 'LibraryDashboardScreen'

    def switch_log_in_screen(self):
        connection = sqlite3.connect("school.db")
        cursor = connection.cursor()
        data_query = "DROP TABLE user"
        cursor.execute(data_query)
        connection.commit()
        cursor.close()
        connection.close()

        _create_local_db()
        self.root.current = 'LogInScreen'


if __name__ == '__main__':
    _create_local_db()
    from kivy.core.window import Window
    Window.size = (400, 650)
    SchoolApp().run()



