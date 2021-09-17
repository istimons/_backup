import sqlite3
from abc import ABC

from threading import Thread
from time import sleep
from kivymd.toast import toast
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFlatButton
from kivy.clock import mainthread
from kivy.gesture import GestureDatabase
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivy.metrics import *
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import ILeftBodyTouch, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivy.factory import Factory
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior


searchBarData = ['school', 'library', 'management', 'with', 'search', 'capability']

''' Start with a DataBase, create one if it does not exist. '''

try:
    connection = sqlite3.connect("school.db")
    cursor = connection.cursor()

    cursor.execute(""" CREATE table Tasks
     (title nvarchar,
     overall INTEGER,
     currency varchar,
     description varchar,
     main varchar)
     """)

    cursor.execute(""" CREATE TABLE Users
        (username varchar   NOT NULL,
        password varchar NOT NULL)        
        """)

    connection.commit()
    cursor.close()
    connection.close()
except sqlite3.OperationalError:
    pass


# ----- Recycle view options------- #

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableButton(RecycleDataViewBehavior, TwoLineAvatarIconListItem):
    """ Add selection support to the Label """

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add Selection on touch down """
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """


# ----- Recycle view options end------- #

class PhoneUpdateDialog(BoxLayout):
    """ Show a pop up dialog to update phone number to the database """


class PasswordUpdateDialog(BoxLayout):
    """ Show a pop up dialog to update password to the database """


class PasswordPhoneUpdateScreen(ThemableBehavior, MDScreen):
    """ Ability of users to change their passwords """

    def __init__(self, **kwargs):
        super(PasswordPhoneUpdateScreen, self).__init__(**kwargs)


class PasswordPhoneBoxUpdate(BoxLayout):
    """ Password change ability container """


class CatalogSearchScreen(ThemableBehavior, MDScreen):
    """ Dashboard class for items Catalog search """

    def __init__(self, **kwargs):
        super(CatalogSearchScreen, self).__init__(**kwargs)


class CatalogSearchBoxScreen(BoxLayout):
    """

    Displays catalog search items.

    """

    search_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(CatalogSearchBoxScreen, self).__init__(**kwargs)

    def set_items_list(self, text="", search=False):
        """ Builds a list of items for the screen """

        def add_item(item_name):

            self.ids.search_results_list.data.append(
                {
                    "viewclass": "SelectableButton",
                    "text": item_name,
                }
            )

        self.ids.search_results_list.data = []
        for item_name in searchBarData:
            if search:
                if text in item_name:
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


class LogInScreen(ThemableBehavior, MDScreen):
    password_entered = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def switch_to_dashboard_screen(self):
        self.parent.current = 'LibraryDashboardScreen'

    def get_user_password(self):
        """ implement MongoDB connection to users that already has access their account"""
        # password_entry = self.password_entered
        self.switch_to_dashboard_screen()

        # try:
        #     connection_user = sqlite3.connect("school.db")
        #     cursor_user_passwd = connection_user.cursor()
        #     cursor_user_passwd.execute("SELECT username, password from Users")
        #     user_data = cursor_user_passwd.fetchall()
        #
        #     passwd = user_data[0][1]  # add more marching conditions
        #     print('current password is %s' % passwd)
        #     if passwd != password_entry.text or len(passwd) == 0:
        #         wrong_password_dialog = MDDialog(text="Wrong Password")
        #         wrong_password_dialog.radius = [20, 7, 20, 7]
        #         wrong_password_dialog.size_hint_x = dp(0.5)
        #         wrong_password_dialog.open()
        #     else:
        #         success_dialog = MDDialog(text="Success!")
        #         success_dialog.radius = [20, 7, 20, 7]
        #         success_dialog.size_hint_x = dp(0.4)
        #         success_dialog.open()
        #         self.switch_to_dashboard_screen()

        # except IndexError:
        #     pass


class SchoolApp(MDApp):
    """ Main class Application """

    dialog = None

    def __init__(self, **kwargs):
        super(SchoolApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Indigo"

    def switch_to_catalog_screen(self):
        self.root.current = 'CatalogSearchScreen'

    def switch_to_password_screen(self):
        self.root.current = 'PasswordPhoneUpdateScreen'

    def switch_to_dashboard_screen(self):
        self.root.current = 'LibraryDashboardScreen'

    def show_phone_update_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Update Phone:",
                type="custom",
                content_cls=PhoneUpdateDialog(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()

    def show_password_update_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Update Password:",
                type="custom",
                content_cls=PasswordUpdateDialog(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()


if __name__ == '__main__':
    from kivy.core.window import Window
    Window.size = (400, 650)
    SchoolApp().run()
