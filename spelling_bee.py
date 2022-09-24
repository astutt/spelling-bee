import streamlit as st

import random
from random import sample
import dataclasses
import string

#~~~~~~~~~~~~~~~~~#todo#~~~~~~~~~~~~~~~~~#
# make it so get_wordlist doesn't run every new game (on solve for valid words)
# make it smarter at picking letters! too hard rn!
# get an easier word list, this one is wild
# make the imterface cuter
# add in a shuffle letters function
# find pangrams, do something exciting for those
### add in more logic for why a guess is invalid, not enough letters, doesn't contain center letter, contains letters not in the 7
# make a progress bar to go with statements, make it look cute
# choose difficulty, based on word list, letters generated, etc. 
# make it so when you win, the try a word input goes away
# give extra points for longer words, and pangrams

MIN_LENGTH = 4 # words must be >=4 letters in the spelling bee
NUM_LETTERS = 7
ALPHABET = string.ascii_lowercase
VOWELS = 'aeiou'
CONSONANTS = ''.join(set(ALPHABET) - set(VOWELS))

# Function to get list of words
@st.cache # The `@streamlit.cache` decorate ensures that this only needs to happen once
def get_wordlist() -> list:
    with open('words.txt') as f: #words.txt, words1000.txt
        wordlist = [line.strip() for line in f]

    wordlist = [w for w in wordlist if MIN_LENGTH <= len(w)]
    wordlist = [w for w in wordlist if all('a' <= c <= 'z' for c in w)]

    return wordlist

# GameState class stores all game attribute as streamlit state
@dataclasses.dataclass
class GameState:
    game_number: int          # how many games you've attempted
    letters: str              # [0] is center letter, [1:] are 6 outside letters
    valid_words: tuple #= ()   # words that pass the test, for this set of letters
    found_words: tuple = () # words they've guessed correctly
    game_over: bool = False   # have you won?

# get list of 7 random letters
# random choice of 2-3 vowels
def get_rand_letters():
    num_vowels = random.choice(range(2,4))
    letters = random.sample(VOWELS,num_vowels)
    letters += random.sample(CONSONANTS,NUM_LETTERS-num_vowels)
    letters_list = list(letters)
    random.SystemRandom().shuffle(letters_list)
    letters = ''.join(letters_list)

    return letters

# generate the list of acceptable words
def solve_spelling_bee(letters: str):

    wordlist = get_wordlist()
    center_letter = letters[0]
    other_letters = letters[1:]

    invalid_letters = [l for l in ALPHABET if l not in letters]
    valid_words = []

    for word in wordlist: # note: len(word) > 3 taken care of in get_wordlist()
        if center_letter in word: # contains center letter
            if word not in valid_words: # not a repeat
                if any(l in invalid_letters for l in word) == False: # doesn't contain any letters not in the special 7
                    valid_words.append(word)
    return tuple(valid_words)

#~~~~~~~~~~~~~~~~~~~~~~~~
@st.cache(allow_output_mutation=True)
def persistent_game_state() -> GameState:
    let = get_rand_letters()
    return GameState(0,let,solve_spelling_bee(let)) # If you wanted to generate letters, instead of asking for them, do that here

state = persistent_game_state()
#~~~~~~~~~~~~~~~~~~~~~~~~

# Write out the game rules
st.write("***Spelling Bee***")
st.write("I'll choose a set of 7 letters, with one being "
         "the special bolded letter. You'll try to come up "
         "with all the words that are only made up of those "
         "7 letters, and each word must contain the bolded "
         "letter. Additionally, all words must be greater "
         "than 3 letters long. If you guess all my words, "
         "you become the queen bee.")

# New game button
if st.button("new game"):
    state.game_number += 1      # add to game count
    state.letters = get_rand_letters()
    state.valid_words = solve_spelling_bee(state.letters)
    state.found_words = ()    # clear this list
    state.game_over = False

# show the letters
st.write(f'Letters: **{state.letters[0]}**, {state.letters[1:]}')

# start taking guesses
if not state.game_over:
    guess = st.text_input('guess a word', key=state.game_number)

    if not guess:
        st.write("don't bee shy")
    elif guess in state.found_words:
        st.write(f'you already have **{guess}**')
    elif guess not in state.valid_words:
        st.write("that's not a valid word, silly")
    else:
        st.write('ur so smart, good job')
        state.found_words += (guess,)

# if you win ...
if all(w in state.found_words for w in state.valid_words):
    st.markdown('**YOU WIN: ur the queen bee**')
    state.game_over = True
# give up, bc the long word list is insane
elif st.button("🛑  i give up  🛑"):
    st.markdown(f"answer: {', '.join(state.valid_words)}")
    st.markdown('**you lose** 😖')
    state.game_over = True

# show your list of found words
st.text(f"you've found these so far: {', '.join(state.found_words)}")

# show progress statement
# rankings: egg, larva, pupa, drone, workerbee, win=queen
num_rankings = 5
num_valid = len(state.valid_words)
num_found = len(state.found_words)
split = num_valid/num_rankings
if num_found < split:
    st.write('Ranking: egg')
elif num_found < 2*split:
    st.write('Ranking: larva')
elif num_found < 3*split:
    st.write('Ranking: pupa')
elif num_found < 4*split:
    st.write('Ranking: drone')
elif num_found < 5*split:
    st.write('Ranking: worker')


# show answers for debugging
st.write(state.valid_words)