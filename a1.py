"""
Wordle
Assignment 1
Semester 1, 2022
CSSE1001/CSSE7030
"""

from string import ascii_lowercase
from typing import Optional

from a1_support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)

__author__ = "Tegjeet Bains, 47453807"
__email__ = "s4745380@student.uq.edu.au"

WORD_LENGTH = 6
MAX_GUESSES = 6


def has_won(guess: str, answer: str) -> bool:
    """Determines if user has won by comparing entered guess and answer for round.

    Parameters:
        guess (str): User's entered guess.
        answer (str): Answer for round.

    Returns:
        bool: True or false whether guess matches answer exactly.
    """
    return guess == answer


def has_lost(guess_number: int) -> bool:
    """Determines if user has lost based on number of guesses inputted.

    Parameters:
        guess_number (int): The guess number of the user.

    Returns:
        bool: True or false whether guess number is greater than or equal to 6.
    """
    return guess_number >= MAX_GUESSES


def remove_word(words: tuple[str, ...], word: str) -> tuple[str, ...]:
    """Removes chosen word from list of possible words.

    Parameters:
        words (tuple<str>): Tuple containing all words
        word (str): Word to be removed

    Returns:
        tuple<str>: New tuple containing all words except removed word
    """
    to_be_removed_idx = words.index(word)
    return words[:to_be_removed_idx] + words[to_be_removed_idx + 1:]


def prompt_user(guess_number: int, words: tuple[str, ...]) -> str:
    """Prompts and reprompts user for a valid guess and returns input.

    Parameters:
        guess_number (int): Integer representing guess number.
        words (tuple<str>): Tuple containing all possible guesses.

    Returns:
        str: User's entered guess.
    """
    while True:
        guess = input(f"Enter guess {guess_number}: ").lower()

        if guess in ("q", "k", "h"):
            return guess
        elif len(guess) != WORD_LENGTH:
            print(f"Invalid! Guess must be of length {WORD_LENGTH}")
        elif guess not in words:
            print("Invalid! Unknown word")
        else:
            return guess


def process_guess(guess: str, answer: str) -> str:
    """Processes user's entered guess and compares with answer to return a modified
    representation of coloured boxes indicating game progress.

    Parameters:
        guess (str): User's entered guess.
        answer (str): Answer for round.

    Returns:
        str: User's entered guess in modified form.
    """
    result = [INCORRECT] * WORD_LENGTH  # initial state is all incorrect
    matched = []

    for i in range(WORD_LENGTH):
        if guess[i] == answer[i]:  # correct letter and position - green
            result[i] = CORRECT
            matched.append(guess[i])

    for i in range(WORD_LENGTH):
        if result[i] == CORRECT:
            continue
        if guess[i] in answer and guess[i] not in matched:  # correct letter and wrong position - yellow
            if guess.count(guess[i]) <= answer.count(guess[i]):
                result[i] = MISPLACED
                matched.append(guess[i])

    return "".join(result)


def update_history(
    history: tuple[tuple[str, str], ...], guess: str, answer: str
) -> tuple[tuple[str, str], ...]:
    """Returns a copy of most up to date user guess history, including guess
    and corresponding coloured boxes.

    Parameters:
        history (tuple(tuple<str,str>)): Tuple containing smaller tuples of guess and
            corresponding coloured boxes.
        guess (str): User's entered guess
        answer (str): Answer for round

    Returns:
        tuple(tuple<str, str>, ...): Updated guess history.
    """
    return history + ((guess, process_guess(guess, answer)),)


def print_history(history: tuple[tuple[str, str], ...]) -> None:
    """Prints user guess history in user-friendly way.

    Parameters:
        history (tuple(tuple(<str, str>))): Tuple containing smaller tuples of guess
            and corresponding coloured boxes.
    """
    for i, (guess, feedback) in enumerate(history, 1):
        print("---------------")
        print(f"Guess {i}:  {' '.join(guess)}")
        print(f"         {feedback}")
    print("---------------\n")


def print_keyboard(history: tuple[tuple[str, str], ...]) -> None:
    """Displays keyboard in a user friendly manner with known information about each letter.

    Parameters:
        history (tuple(tuple(<str, str>))): Tuple containing smaller tuples of
            guess and corresponding coloured boxes.
    """
    alphabet = list(ascii_lowercase)
    status = [" "] * 26

    for guess, feedback in history:
        for i in range(WORD_LENGTH):
            idx = alphabet.index(guess[i])
            if status[idx] == " " or (status[idx] == MISPLACED and feedback[i] == CORRECT):
                status[idx] = feedback[i]

    print("\nKeyboard information")
    print("------------")
    for i in range(0, 26, 2):
        print(f"{alphabet[i]}: {status[i]}\t{alphabet[i+1]}: {status[i+1]}")
    print()


def print_stats(stats: list[int]) -> None:
    """Prints user stats in a user-friendly manner.

    Parameters:
        stats (list<int>): List with 7 integer elements that indicate amount
            of times game won in 1-6 moves and games lost.
    """
    print("\nGames won in:")
    for i in range(MAX_GUESSES):
        print(f"{i+1} moves: {stats[i]}")
    print(f"Games lost: {stats[6]}")


def main():
    """Utilises functions above to co-ordinate gameplay."""
    vocab = load_words(VOCAB_FILE)      # all 6-letter words
    answers = load_words(ANSWERS_FILE)  # 6-letter possible answers
    stats = [0] * 7  # reset stats
    playing = True

    while playing:
        # choose word to be guessed and initialise appropriate variables
        answer = choose_word(answers)
        answers = remove_word(answers, answer)

        history = ()
        guess_number = 1
        round_active = True

        while round_active:
            guess = prompt_user(guess_number, vocab)

            if guess == "q":  # quit
                playing = False
                break
            elif guess == "k":  # keyboard status
                print_keyboard(history)
                continue
            elif guess == "h":  # help
                print("Ah, you need help? Unfortunate.")
                continue

            history = update_history(history, guess, answer)
            print_history(history)  # display guesses

            if has_won(guess, answer):
                print(f"Correct! You won in {guess_number} guesses!")
                stats[guess_number - 1] += 1
                round_active = False
            elif has_lost(guess_number):
                print(f"You lose! The answer was: {answer}")
                stats[6] += 1
                round_active = False

            guess_number += 1

        if playing:
            again = input("Would you like to play again (y/n)? ").lower()
            if again != "y":
                playing = False

    print_stats(stats)


if __name__ == "__main__":
    main()
