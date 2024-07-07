from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget




class MenuWidget(RelativeLayout):
    #from main import MainWidget
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)