import arcade
from arcade.gui import (
    UIManager,
    UIAnchorLayout, 
    UIFlatButton,
    UITextureButton,
    UIBoxLayout,
    UIInputText,
    UIOnChangeEvent
)
from resources.constants.constants import LIST_OF_KEYS
from logic.game_logic import GameLogic
from pathlib import Path

TEX_RED_BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.CADMIUM_GREEN)

        self.game_logic = GameLogic()
        self.setup()

        font_file_path = Path('resources/fonts/PermanentMarker-Regular.ttf')
        arcade.load_font(font_file_path)

        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout())

        self.box_layout = UIBoxLayout(space_between=20, vertical=False)
        self.anchor.add(self.box_layout, anchor_x="center", anchor_y="bottom", align_y=100)

        guess_letter_button = self.box_layout.add(
            UITextureButton(
                text="Guess the letter",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_pressed=TEX_RED_BUTTON_PRESS,
                texture_hovered=TEX_RED_BUTTON_HOVER
            ),
        )
        guess_word_button = self.box_layout.add(
            UITextureButton(
                text="Guess the word",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_pressed=TEX_RED_BUTTON_PRESS,
                texture_hovered=TEX_RED_BUTTON_HOVER
            )
        )

        self.text_input = UIInputText(text="Make a guess", width=300)
        self.text_input_visible = False
        self.guessed_letter = ''

        @self.text_input.event('on_click')
        def on_click(event):
            self.text_input.text = ''

        @self.text_input.event('on_change')
        def on_change(event: UIOnChangeEvent):
            if not event.new_value.isalpha() or len(event.new_value) > 1:
                self.text_input.invalid = True
                self.text_input.text = ''
            else:
                self.text_input.invalid = False
                self.guessed_letter = event.new_value.lower()

        @guess_letter_button.event("on_click")
        def on_click(event):
            if not self.text_input_visible:
                self.anchor.add(self.text_input, anchor_x='center', anchor_y='center', align_y=-100)
                self.text_input_visible = True
            else:
                self.anchor.remove(self.text_input)
                self.text_input_visible = False
            self.ui.trigger_render()

        @guess_word_button.event("on_click")
        def on_click(event):
            print(event)

        # self.random_text = arcade.Text("WAR", x=100, y=100, color=arcade.color.CAMOUFLAGE_GREEN, font_name=('Permanent Marker'), font_size=20)

    def setup(self):
        self.game_logic.reset()
        self.game_logic.generate_word()
        self.generate_word_list()

    def generate_word_list(self):
        letter_width = 50
        underscore_width = 40 
        start_y = self.window.height / 2

        total_width = (len(self.game_logic.word) - 1) * letter_width + underscore_width 
        start_x = (self.window.width - total_width) / 2

        letter_lines = []
        for i in range(len(self.game_logic.word)):
            x = start_x + i * letter_width
            letter_lines.append({
                'x': x, 
                'y': start_y, 
                'letter': self.game_logic.word[i], 
                'guessed': False
            })
            # lines.append((x, start_y))
            # lines.append((x + underscore_width, start_y))
        self.letter_lines = letter_lines

    def on_guess_letter(self):
        self.game_logic.guess_letter(self.guessed_letter)

        for index, elm in enumerate(self.game_logic.user_progress):
            if elm:
                self.letter_lines[index]['guessed'] = True

    
    def on_draw(self): # this is a function used to draw sprites, text anything on the screen basically.
        self.clear()

        self.handle_word_line_draw()
        self.draw_wrong_guessed_letters()

        for item in self.wrong_guessed_letters:
            item.draw()

        self.ui.draw()
        # arcade.draw_lines(self.lines, arcade.color.ALLOY_ORANGE, 5)            
        
        # self.random_text.draw()

    def draw_wrong_guessed_letters(self):
        corner_distance = 50
        self.wrong_guessed_letters = []

        for index, letter in enumerate(self.game_logic.wrong_guessed_letters):
            self.wrong_guessed_letters.append(arcade.Text(
                letter.upper(),
                corner_distance * (index + 1),
                self.window.height - corner_distance,
                font_name="Permanent Marker",
                font_size=18
            ))

    def handle_word_line_draw(self):
        underscore_width = 40
        if self.letter_lines:
            for item in self.letter_lines:
                if item['guessed']:
                    arcade.draw_text(item['letter'].upper(), item['x'] + underscore_width / 3, item['y'], color=arcade.color.WHITE_SMOKE, font_size=18, font_name="Permanent Marker")
                else:
                    arcade.draw_line(item['x'], item['y'], item['x'] + underscore_width, item['y'], color=arcade.color.BLACK_LEATHER_JACKET, line_width=4)
                

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_key_press(self, symbol,  modifiers):
        if symbol == arcade.key.ENTER and not self.text_input.invalid:
            print("TEXT", self.text_input.text)
            self.anchor.remove(self.text_input)
            self.text_input_visible = False
            self.ui.trigger_render()

            self.on_guess_letter()

