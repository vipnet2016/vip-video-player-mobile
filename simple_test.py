"""
Simple test app for verifying build process
"""
from kivy.app import App
from kivy.uix.label import Label

class SimpleTestApp(App):
    def build(self):
        return Label(text='Build Test Successful!')

SimpleTestApp().run()