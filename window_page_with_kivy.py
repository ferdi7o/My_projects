from kivy.app import App
from kivy.uix.label import Label

class Myapp(App):
    def build(self):
        return Label(text = "Page with Kivy")


Myapp().run()