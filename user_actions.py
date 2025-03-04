from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):

    self._keyboard = None
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    """if keycode[1] == 'space':
        self.on_pause_button_pressed_desactived()"""
    if keycode[1] == 'left' and not self.button_pause:
        self.current_speed_x = self.SPEED_X
    elif keycode[1] == 'right' and not self.button_pause:
        self.current_speed_x = -self.SPEED_X
    return True

def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0

def on_touch_down(self, touch):
    """if not self.button_pause:
        self.current_speed_x = 0"""
    if not self.state_game_over and self.state_game_has_started:
        if touch.x < self.width/2 and not self.button_pause:
            self.current_speed_x = self.SPEED_X
        else:
            if not self.button_pause:
                self.current_speed_x = - self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    self.current_speed_x = 0
