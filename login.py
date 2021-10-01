from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.factory import Factory


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal" # BlueGray
        return Builder.load_file('login.kv')
MainApp().run()

