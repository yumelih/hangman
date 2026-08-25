import arcade
from views.game_view import GameView
from resources.constants.constants import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH


arcade.load_font('resources/fonts/PermanentMarker-Regular.ttf')


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.total_score = 0
    window.show_view(GameView())
    arcade.run()


if __name__ == "__main__":
    main()
