import random
from english_dictionary.scripts.read_pickle import get_dict
from enum import Enum

class Status(Enum):
    SUCCESS = 0,
    FAILED = 1,
    ALREADY_GUESSED = 2,
    LETTER_DONT_EXIST = 3,
    WORD_DONT_MATCH = 4,
    CORRECT_LETTER_GUESS = 5


class GameLogic():
    MAXIMUM_TRIES = 6
    english_dict = get_dict()
    def __init__(self):
        self.word = ''
        self.user_progress = []
        self.wrong_guessed_letters = []
        self.wrong_guessed_words = []

    def get_fail_count(self):
        return len(self.wrong_guessed_letters) + len(self.wrong_guessed_words)

    def generate_word(self):
        self.word = random.choice(list(GameLogic.english_dict.keys())).lower()
        self.user_progress = [None] * len(self.word)

    def guess_letter(self, letter: str):
        if self.wrong_guessed_letters.count(letter) != 0 or self.user_progress.count(letter) != 0:
            return Status.ALREADY_GUESSED
        
        if self.word.find(letter) == -1:
            self.wrong_guessed_letters.append(letter)
            return self.check_is_failed(Status.LETTER_DONT_EXIST)
        
        for i in range(len(self.user_progress)):
            if self.word[i] == letter:
                self.user_progress[i] = letter

        if None not in self.user_progress:
            return Status.SUCCESS

        return Status.CORRECT_LETTER_GUESS

    def guess_word(self, guess_word):
        if self.wrong_guessed_words.count(guess_word.lower()) != 0:
            return Status.ALREADY_GUESSED

        if self.word != guess_word:
            self.wrong_guessed_words.append(guess_word)
            return self.check_is_failed(Status.WORD_DONT_MATCH)

        self.user_progress = list(self.word)
        
        return Status.SUCCESS

    def check_is_failed(self, custom_error):
        fail_rate = len(self.wrong_guessed_letters) + len(self.wrong_guessed_words)
        if(fail_rate >= GameLogic.MAXIMUM_TRIES):
            return Status.FAILED
        return custom_error

    def calculate_score(self, earlier_user_progress, is_word_guess: bool = False):
        score = 10
        points_for_letter = 5
        points_for_wrong_guess = 2
        one_hit = 20

        number_of_missing_letters = earlier_user_progress.count(None)
        completed_letter_score = number_of_missing_letters * points_for_letter
        score += completed_letter_score

        score -= (points_for_wrong_guess * self.get_fail_count())

        if is_word_guess and number_of_missing_letters == len(self.word):
            score += one_hit


        print("SCORE", number_of_missing_letters, completed_letter_score)

        return score
            

    def reset(self):
        self.word = ''
        self.wrong_guessed_letters = []
        self.user_progress = []