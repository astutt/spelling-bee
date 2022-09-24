# Testing game logic, can delete later

import string
import random
from random import sample

MIN_LENGTH = 4
NUM_LETTERS = 7
ALPHABET = string.ascii_lowercase
VOWELS = 'aeiou'
CONSONANTS = ''.join(set(ALPHABET) - set(VOWELS))

def get_wordlist() -> list:
    with open('spelling-bee/words.txt') as f: # change path for streamlit vs. not
        wordlist = [line.strip() for line in f]

    wordlist = [w for w in wordlist if MIN_LENGTH <= len(w)]
    wordlist = [w for w in wordlist if all('a' <= c <= 'z' for c in w)]

    return wordlist

wordlist = get_wordlist()

num_vowels = random.choice(range(2,5))
letters = random.sample(VOWELS,num_vowels)
letters += random.sample(CONSONANTS,NUM_LETTERS-num_vowels)

letters_list = list(letters)
random.SystemRandom().shuffle(letters_list)
letters = ''.join(letters_list)

center_letter = letters[0]
other_letters = letters[1:]

invalid_letters = [l for l in ALPHABET if l not in letters]
valid_words = []

for word in wordlist: # note: len(word) > 3 taken care of in get_wordlist()
    if center_letter in word: # contains center letter
        if word not in valid_words: # not a repeat
            if any(l in invalid_letters for l in word) == False: # doesn't contain any letters not in the special 7
                valid_words.append(word)

num_words = len(valid_words)

if 

print(tuple(valid_words))
print(num_words)