# Hangman

A Python implementation of Hangman, with word data pulled from `english_dictionary` and a scoring system for letter/word guesses.

## Features

- Random word selection from an English dictionary package
- Letter and full-word guessing
- Status tracking via an `Enum` (`SUCCESS`, `FAILED`, `ALREADY_GUESSED`, `LETTER_DONT_EXIST`, `WORD_DONT_MATCH`, `CORRECT_LETTER_GUESS`)
- Scoring based on remaining letters, wrong guesses, and one-shot word guesses
- Max of 6 wrong guesses before the game ends

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) for dependency management and running the project

## Setup

Clone the repo and install dependencies with uv:

```bash
uv sync
```

## Usage

Run the game with:

```bash
uv run main.py
```

## How It Works

- `generate_word()` picks a random word and resets progress
- `guess_letter(letter)` checks a single letter against the word
- `guess_word(word)` checks a full-word guess
- `calculate_score(...)` computes points based on progress and mistakes
- `reset()` clears state for a new round
