import random
from string import ascii_lowercase

WORDLIST_FILENAME = "words.txt"


def load_words():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    return set(secret_word).issubset(set(letters_guessed))



def get_guessed_word(secret_word, letters_guessed):
    row = list('_' * len(secret_word))
    for i in range(0, len(secret_word)):
        for j in range(0, len(letters_guessed)):
            if letters_guessed[j] == secret_word[i]:
                row[i] = secret_word[i]
                break
    return ' '.join(row)



def get_available_letters(letters_guessed):
    return ''.join(sorted(list(set(ascii_lowercase) - set(letters_guessed))))


set_with_repeated = []
SET_WITH_USED_LETTERS = []


def value_func(warnings):
    try:
        global set_with_repeated, SET_WITH_USED_LETTERS
        letter_to_join = input('Print your letter:')[0]
        if letter_to_join in SET_WITH_USED_LETTERS:
            warnings -= 1
            print('Warning, you used this letter')
            set_with_repeated.append(letter_to_join)
            return value_func(warnings)
        elif letter_to_join.istitle():
            letter_to_join = letter_to_join.lower()
        elif not letter_to_join.isalpha():
            print('Invalid input')
            return value_func(warnings)
    except IndexError:
        print('Invalid length')
        return value_func(warnings)

    return letter_to_join, warnings



def hangman(secret_word):
    global SET_WITH_USED_LETTERS, set_with_repeated
    word = '_' * len(secret_word)
    counter_of_trials, warnings = 6, 3

    print(f"""Welcome to Hangman
    I am thinking of a word that is {len(secret_word)} letters long
    You have counters {counter_of_trials} guesses left
    Available letters: {get_available_letters(SET_WITH_USED_LETTERS)} """)


    while counter_of_trials > 0:
        guested = len(secret_word)
        letter_to_join, warnings = value_func(warnings)
        if letter_to_join not in secret_word:
            print('Your guess is wrong')
            counter_of_trials -= 1
        SET_WITH_USED_LETTERS = list(set(SET_WITH_USED_LETTERS + list(letter_to_join)))
        word = get_guessed_word(secret_word, SET_WITH_USED_LETTERS)
        print(word)

        if is_word_guessed(secret_word, word):
            break

        if 0 < warnings < 3:
            print(f'You have only {warnings} warnings left')
        elif warnings < 1:
            counter_of_trials -= 1

    print(f'''I am thinking of a word that is {len(secret_word)} letters long
    You have counters {counter_of_trials} guesses left
    Available letters: {get_available_letters(SET_WITH_USED_LETTERS)}
    -------------------------------------------''')

    if is_word_guessed(secret_word, word):
        print('You won, congratulations!')
    else:
        print(f'''Sorry, you ran out of guessses.
    The right word is {secret_word}
    Your total score for this game is: {(len(SET_WITH_USED_LETTERS)-len(set_with_repeated)) * counter_of_trials}''')

    return (len(SET_WITH_USED_LETTERS) - len(set_with_repeated)) * counter_of_trials




wordlist = load_words()

if __name__ == "__main__":

    secret_word = choose_word(wordlist)
    hangman(secret_word)
