import random
import time

from kivy import platform
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Config.set("graphics", "width", "1000")
Config.set("graphics", "height", "400")
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty, BooleanProperty

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    from better_score import get_better_score, write_score
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    menu_widget = ObjectProperty()
    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")
    pause = StringProperty("")
    backgroung_button_pause = ObjectProperty((0, 0, 0, 1))
    backgroung_pause = ObjectProperty((0, 0, 0, .0000000000001))
    text_button_pause = StringProperty("")
    decompt = StringProperty("")
    go_decompt = BooleanProperty(False)
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    score_txt = NumericProperty(0)
    score_better_txt = NumericProperty(0)
    score_better = NumericProperty(0)
    V_NB_LINES = 12
    V_LINES_SPACING = .25
    vertical_lines = []
    H_NB_LINES = 100
    SPEED_Y = 100
    H_LINES_SPACING = .15
    horizontal_lines = []
    current_offset_y = 0
    SPEED_X = 3.0
    current_offset_x = 0
    current_speed_x = 0
    current_y_loop = 0
    tiles_coordinates = []
    tiles = []
    NB_TILES = 4
    tile = None
    ship = None
    SHIP_WIDTH = .1
    SHIP_HEIGHT = .035
    SHIP_BASE_Y = .04
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]
    state_game_over = False
    state_game_has_started = False
    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None
    button_pause = False
    start = False
    sound_pos = 0
    num = 20
    k = 1.2
    i = 3

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        #self.get_better_score()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.init_audio()
        #self.button_pause_function()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.sound_galaxy.play()
        self.score_better = int(self.get_better_score())

    def reset_game(self):
        self.current_offset_y = 0
        self.SPEED_X = 3.0
        self.current_offset_x = 0
        self.current_speed_x = 0
        self.current_y_loop = 0
        self.SPEED_Y = .5
        self.tiles_coordinates = []
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False
        self.score_txt = self.current_y_loop

    def init_audio(self):
        self.num = random.randint(1, 30)
        print(self.num)
        self.sound_begin = SoundLoader.load('RESSOURCES/audio/begin.wav')
        self.sound_galaxy = SoundLoader.load('RESSOURCES/audio/galaxy.wav')
        self.sound_gameover_impact = SoundLoader.load('RESSOURCES/audio/gameover_impact.wav')
        self.sound_gameover_voice = SoundLoader.load('RESSOURCES/audio/gameover_voice.wav')
        self.sound_music1 = SoundLoader.load("RESSOURCES/audio/music" + str(self.num) +".wav")
        #self.sound_decompt = SoundLoader.load("RESSOURCES/audio/sound_decompt.mp3")
        self.sound_restart = SoundLoader.load('RESSOURCES/audio/restart.wav')
        self.sound_begin.volume = 1
        self.sound_galaxy.volume = .25
        self.sound_gameover_impact.volume = .6
        self.sound_gameover_voice.volume = .25
        self.sound_music1.volume = .25
        self.sound_restart.volume = .25
        #self.sound_decompt.volume = .25


    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width/2
        base_y = self.SHIP_BASE_Y * self.height
        half_width = self.SHIP_WIDTH * self.width/2
        ship_height = self.SHIP_HEIGHT*self.height
        self.ship_coordinates[0] = center_x - half_width, base_y
        self.ship_coordinates[1] = center_x, base_y + ship_height
        self.ship_coordinates[2] = center_x + half_width, base_y
        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])
        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x+1, ti_y+1)
        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1, .4)
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1, .4)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index-0.5
        line_x = central_line_x + offset*spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0]+1, tile_coordinates[1]+1)
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)
            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        start_index = - int(self.V_NB_LINES/2) + 1
        for i in range(start_index, start_index+self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(x1, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        start_index = - int(self.V_NB_LINES/2) + 1
        end_index = start_index + self.V_NB_LINES - 1
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def pre_fill_tiles_coordinates(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        last_y = 0
        last_x = 0

        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]
        if len(self.tiles_coordinates) > 0:
            last_coordinate = self.tiles_coordinates[-1]
            last_y = last_coordinate[1] + 1
            last_x = last_coordinate[0]

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)
            start_index = - int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 1
            if last_x <= start_index:
                r = 1
            if last_x >= end_index-1:
                r = 2
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def update(self, dt):
        if self.score_txt % 300 == 0 and self.score_txt != 0:
            self.k += 0.009
        time_factor = dt*60
        speed_y = self.SPEED_Y * self.height*self.k
        speed_x = self.current_speed_x * self.width
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            self.current_offset_y += speed_y * time_factor/100
            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = self.current_y_loop
                self.score_better_txt = self.score_better
                if self.score_txt > self.score_better_txt:
                    self.score_better_txt = self.score_txt
                    self.write_score(self.score_better_txt)
                """if self.score_txt == 20 and self.check_ship_collision():
                    print("dvv")
                    self.num += 1
                    self.init_audio(self.num)
                    self.state_game_over = True
                    self.menu_widget.opacity = 1
                    self.menu_title = "G  A  M  E    O  V  E  R"
                    self.sound_music1.stop()
                    self.sound_gameover_impact.play()
                    Clock.schedule_once(self.play_voice_game_over, 3)
                    self.menu_button_title = "RESTART"""""

                """if self.score_txt == 20 and self.check_ship_collision():
                    print("dvv")
                    self.num += 1
                    self.sound_music1.stop()
                    self.sound_music1 = SoundLoader.load("RESSOURCES/audio/music" + str(self.num) + ".wav")
                    self.sound_music1.play()"""
                self.generate_tiles_coordinates()
            self.current_offset_x += speed_x * time_factor/100
            self.pause = "PAUSE"
        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            #self.start = False
            self.backgroung_button_pause = (0, 0, 0, 1)
            self.text_button_pause = ""
            self.menu_widget.opacity = 1
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            Clock.schedule_once(self.play_voice_game_over, 2)
            self.menu_button_title = "RESTART"
            self.pause = ""

    def play_voice_game_over(self, dt):
        if self.state_game_over:
            self.sound_gameover_voice.play()

    def on_pause_button_pressed_actived(self):
        #self.menu_title = "E  N    P  A  U  S  E"
        self.SPEED_Y = 0
        self.current_speed_x = 0
        self.button_pause = True
        self.backgroung_button_pause = (1, .3, .4)
        self.text_button_pause = "PLAY"
        self.backgroung_pause = ObjectProperty((0, 0, 0, .4))
        self.sound_pos = self.sound_music1.get_pos()
        print(self.sound_pos)
        self.sound_music1.stop()
        #self.menu_button_title = "RESTART"

    def decomp_pause(self, dt):
        if self.i == 1:
            self.decompt = "G O"
        else:
            self.decompt = str(self.i)


    def on_pause_button_pressed_desactived(self, dt):
        self.go_decompt = True
        #self.sound_decompt.play()
        #Clock.schedule_once(self.on_pause_button_pressed_desactived_play, 3)
        self.decomp_pause(dt)
        Clock.schedule_once(self.do_seek, 1/2)
        Clock.schedule_once(self.decomp_pause, 1)
        Clock.schedule_once(self.do_seek, 1)
        Clock.schedule_once(self.decomp_pause, 2)
        Clock.schedule_once(self.on_pause_button_pressed_desactived_play, 2.5)



    def on_pause_button_pressed_desactived_play(self, dt):
        self.i = 3
        self.decompt = ""
        self.go_decompt = False
        #self.menu_title = "E  N    P  A  U  S  E"
        self.backgroung_button_pause = (1, .3, .4)
        self.text_button_pause = "PAUSE"
        """Clock.schedule_once(self.decomp_pause, 1)
        Clock.schedule_once(self.decomp_pause, 1)
        Clock.schedule_once(self.button_pause, 1)"""
        self.button_pause = False
        self.backgroung_pause = ObjectProperty((0, 0, 0, .0000000000001))
        self.SPEED_Y = .5
        self.current_speed_x = 0
        self.sound_music1.play()
        #Clock.schedule_once(self.do_seek)
        #self.menu_button_title = "RESTART"

    def do_seek(self, dt):
        self.i -= 1


    def on_menu_button_pressed(self):
        self.score_better = self.get_better_score()
        #print(score_better)
        self.backgroung_button_pause = (1, .3, .4)
        self.text_button_pause = "PAUSE"
        #self.start = True
        self.k = 1.2
        if self.state_game_over:
            #self.start = True
            self.sound_restart.play()
            self.init_audio()
        else:
            self.sound_begin.play()
            #self.start = True
        self.sound_music1.play()
        #time.sleep(3)
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0
        #self.button_pause_function()

"""class BoxLayoutPause(MainWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if self.state_game_has_started:
        b = Button(text="PAUSE",
        font_size=dp(20),
        font_name="RESSOURCES/fonts/eurostile.ttf",
        bold=True,
        pos_hint={"x": .89, "top": .95},
        size_hint=(.1, .07),
        on_press=self.on_pause_button_pressed_actived() if self.button_pause == False else self.on_pause_button_pressed_desactived(
        self),
        background_normal='', background_color=(1, .3, .4, .95), halign="center",
        valign="center")
        self.add_widget(b)"""


class GalaxyApp(App):
    pass


GalaxyApp().run()