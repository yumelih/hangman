import arcade
from arcade.gui import (
    UIManager,
    UIAnchorLayout, 
    UIFlatButton,
    UITextureButton,
    UIBoxLayout,
    UIInputText,
    UIOnChangeEvent,
    UILabel
)
from resources.constants.constants import LIST_OF_KEYS
from logic.game_logic import GameLogic, Status
from pathlib import Path

TEX_RED_BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")

class GameOverView(arcade.gui.UIView):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BRUNSWICK_GREEN)
        
        self.anchor = UIAnchorLayout()
        self.ui.add(self.anchor)

        self.box_layout = UIBoxLayout(space_between=20)
        self.anchor.add(self.box_layout, anchor_x='center', anchor_y='center')

        title = UILabel('Game Over', width=200, font_size=24, text_color=arcade.color.FLORAL_WHITE)
        total_score = UILabel(f'Total Score: {self.window.total_score}', width=200, font_size=24, text_color=arcade.color.FLORAL_WHITE)
        self.anchor.add(total_score, anchor_x='left', anchor_y='top', align_x=20, align_y=-20)

        self.box_layout.add(title)
        restart_button = self.box_layout.add(
            UITextureButton(
                text="Restart",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_pressed=TEX_RED_BUTTON_PRESS,
                texture_hovered=TEX_RED_BUTTON_HOVER
            ),
        )
        exit_button = self.box_layout.add(
            UITextureButton(
                text="Exit",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_pressed=TEX_RED_BUTTON_PRESS,
                texture_hovered=TEX_RED_BUTTON_HOVER
            )
        )

        @restart_button.event('on_click')
        def restart_button_click(event):
            game_view = GameView()
            self.window.show_view(game_view)

        @exit_button.event('on_click')
        def exit_button_click(event):
            self.window.close()


    def on_draw_before_ui(self):
        arcade.set_background_color(arcade.color.BRUNSWICK_GREEN)

    def on_draw_after_ui(self):
        pass

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

        self.score = 0
        self.score_label = UILabel(text=f"Score: {self.score}", font_size=24, text_color=arcade.color.GHOST_WHITE)
        self.anchor.add(
            self.score_label,
            anchor_x='center', 
            anchor_y='top', 
            align_y=-50
        )

        wrong_guesses_label = UILabel(text=f"Wrong Guesses: ", font_size=24, text_color=arcade.color.GHOST_WHITE)
        self.anchor.add(
            wrong_guesses_label,
            anchor_x='left', 
            anchor_y='top', 
            align_y=-20,
            align_x=20
        )

        correct_guesses_label = UILabel(text=f"Correct Guesses: ", font_size=24, text_color=arcade.color.GHOST_WHITE)
        self.anchor.add(
            correct_guesses_label,
            anchor_x='left', 
            anchor_y='top', 
            align_y=-(self.window.height / 2) - 20,
            align_x=20
        )

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

        self.notify_toast = UILabel(
            text='',
            font_size=24,
            text_color=arcade.color.WHITE,
            width=300,
            align='center'
        )
        self.notify_toast.with_background(color=arcade.color.AIR_FORCE_BLUE)
        self.notify_toast.with_padding(all=20)

        self.notify_toast_visible = False
        self.notify_toast_visible_time = 0.0
        self.TOAST_VISIBLE = 5.0

        self.text_input = UIInputText(text="Make a guess", width=300)
        self.text_input_visible = False
        self.guessed_letter = ''

        self.text_input_word = UIInputText(text="Guess the word", width=300)
        self.text_input_word_visible = False
        self.guessed_word = ''

        @guess_letter_button.event("on_click")
        def on_click(event):
            if self.text_input_word_visible:
                self.anchor.remove(self.text_input_word)
                self.text_input_word_visible = False

            if not self.text_input_visible:
                self.anchor.add(self.text_input, anchor_x='center', anchor_y='center', align_y=-100)
                self.text_input_visible = True
            else:
                self.anchor.remove(self.text_input)
                self.text_input_visible = False
            self.ui.trigger_render()

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


        @guess_word_button.event("on_click")
        def on_click(event):
            if self.text_input_visible:
                self.anchor.remove(self.text_input)
                self.text_input_visible = False

            if not self.text_input_word_visible:
                self.anchor.add(self.text_input_word, anchor_x='center', anchor_y='center', align_y=-100)
                self.text_input_word_visible = True
            else: 
                self.anchor.remove(self.text_input_word)
                self.text_input_visible = False
            self.ui.trigger_render()

        @self.text_input_word.event('on_click')
        def on_click(event):
            self.text_input_word.text = ''

        @self.text_input_word.event("on_change")
        def on_change(event: UIOnChangeEvent):
            if not event.new_value.isalpha():
                self.text_input_word.invalid = True
                self.text_input_word.text = event.new_value[:-1]
            else:
                self.text_input_word.invalid = False
                self.guessed_word = event.new_value.lower()
                self.text_input_word.deactivate()
                self.text_input_word.activate()


    def setup(self):
        self.game_logic.reset()
        self.game_logic.generate_word()
        self.generate_word_list()
        print(self.game_logic.word)

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
        earlier_user_progress = self.game_logic.user_progress
        response = self.game_logic.guess_letter(self.guessed_letter)

        if self.notify_toast_visible:
            self.anchor.remove(self.notify_toast)
            self.ui.trigger_render()

        match response:
            case Status.SUCCESS:
                self.notify_toast.text = 'Success, You Won!'
                self.score += self.game_logic.calculate_score(earlier_user_progress)
                self.window.total_score += self.game_logic.calculate_score(earlier_user_progress)
                self.score_label.text = f"Score: {self.score}"
                self.setup()
            case Status.CORRECT_LETTER_GUESS:
                self.notify_toast.text = 'Correct Guess!'
            case Status.ALREADY_GUESSED:
                self.notify_toast.text = 'Already Guessed the Letter'
            case Status.LETTER_DONT_EXIST:
                self.notify_toast.text = 'Wrong Guess!'
            case Status.FAILED:
                self.notify_toast.text = 'You Lost :('
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
                

        self.anchor.add(self.notify_toast, anchor_x="center", anchor_y="top")
        self.notify_toast_visible = True

        for index, elm in enumerate(self.game_logic.user_progress):
            if elm:
                self.letter_lines[index]['guessed'] = True

    def on_guess_word(self):
        earlier_user_progress = self.game_logic.user_progress
        response = self.game_logic.guess_word(self.guessed_word)

        if self.notify_toast_visible:
            self.anchor.remove(self.notify_toast)
            self.ui.trigger_render()

        match response:
            case Status.SUCCESS:
                self.notify_toast.text = 'Success, You Won!'
                self.score += self.game_logic.calculate_score(earlier_user_progress, True)
                self.window.total_score += self.game_logic.calculate_score(earlier_user_progress, True)
                self.score_label.text = f"Score: {self.score}"
                self.setup()
            case Status.ALREADY_GUESSED:
                self.notify_toast.text = 'Already Guessed the Letter'
            case Status.WORD_DONT_MATCH:
                self.notify_toast.text = 'Wrong Guess!'
            case Status.FAILED:
                self.notify_toast.text = 'You Lost :('
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
        
        self.anchor.add(self.notify_toast, anchor_x="center", anchor_y="top")
        self.notify_toast_visible = True
        
    def on_update(self, delta_time: float):
        if self.notify_toast_visible:
            self.notify_toast_visible_time += delta_time

        if self.notify_toast_visible and self.notify_toast_visible_time > self.TOAST_VISIBLE:
            self.notify_toast_visible = False
    
    def on_draw(self): # this is a function used to draw sprites, text anything on the screen basically.
        self.clear()

        self.handle_word_line_draw()
        self.draw_wrong_guessed_letters()

        for item in self.wrong_guessed_letters:
            item.draw()

        self.draw_wrong_guessed_words()
        for item in self.wrong_guessed_words:
            item.draw()

        self.draw_number_of_mistakes()
        self.number_of_mistakes.draw()

        self.draw_correct_guessed_letters()
        for item in self.correct_guessed_words:
            item.draw()

        if not self.notify_toast_visible and self.notify_toast_visible_time > self.TOAST_VISIBLE:
            self.anchor.remove(self.notify_toast)
            self.notify_toast_visible_time = 0.0
            self.ui.trigger_render()

        self.ui.draw()
        # arcade.draw_lines(self.lines, arcade.color.ALLOY_ORANGE, 5)            
        
        # self.random_text.draw()

    def draw_correct_guessed_letters(self):
        corner_distance_x = 50
        corner_distance_y = (self.window.height / 2) - 100
        distance_between_elm = 20

        self.correct_guessed_words = []
        for index, word in enumerate(self.game_logic.correct_word_guesses):
            self.correct_guessed_words.append(arcade.Text(
                word,
                corner_distance_x,
                corner_distance_y - (index * distance_between_elm),
                font_name="Permanent Marker",
                font_size=16
            )) 

    def draw_wrong_guessed_letters(self):
        corner_distance_x = 50
        corner_distance_y = 90
        self.wrong_guessed_letters = []

        for index, letter in enumerate(self.game_logic.wrong_guessed_letters):
            self.wrong_guessed_letters.append(arcade.Text(
                letter.upper(),
                corner_distance_x * (index + 1),
                self.window.height - corner_distance_y,
                font_name="Permanent Marker",
                font_size=16
            ))

    def draw_wrong_guessed_words(self):
        corner_distance_x = 50
        corner_distance_y = 100
        y_distance = 50
        self.wrong_guessed_words = []

        for index, letter in enumerate(self.game_logic.wrong_guessed_words):
            self.wrong_guessed_words.append(arcade.Text(
                letter.upper(),
                corner_distance_x,
                (self.window.height - corner_distance_y) - (y_distance * (index + 1)) ,
                font_name="Permanent Marker",
                font_size=16
            ))

    def draw_number_of_mistakes(self):
        corner_distance = 50
        self.number_of_mistakes = arcade.Text(
            f"{self.game_logic.get_fail_count()}/{GameLogic.MAXIMUM_TRIES}",
            self.window.width - corner_distance,
            self.window.height - corner_distance,
            font_name="Permanent Marker",
            font_size=18
        )

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
        if symbol == arcade.key.ENTER and not self.text_input.invalid and self.text_input_visible:
            print("TEXT", self.text_input.text)
            self.anchor.remove(self.text_input)
            self.text_input_visible = False
            self.ui.trigger_render()
            self.text_input.text = ''
            self.on_guess_letter()

        if symbol == arcade.key.ENTER and not self.text_input_word.invalid and self.text_input_word_visible:
            self.anchor.remove(self.text_input_word)
            self.text_input_word_visible = False
            self.ui.trigger_render()
            self.text_input_word.text = ''
            self.on_guess_word()
        

