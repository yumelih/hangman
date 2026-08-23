import inspect
from arcade import key

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "HANGMAN"

LIST_OF_KEYS = {
    value: name for name, value in inspect.getmembers(key)
    if len(name) == 1
}
