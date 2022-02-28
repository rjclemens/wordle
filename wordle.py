import math
import itertools as it
import random
from termcolor import colored, cprint

with open('words.txt') as file:
    WORDS = file.read().split(',')

with open('possible_words.txt') as file:
    P_WORDS = file.read().split('\n')

GREY = 0
TAN = 1
GREEN = 2

COLORS = ['on_white', 'on_yellow', 'on_green']

WORDS_SIZE = len(WORDS)
P_WORDS_SIZE = len(P_WORDS)

vals = list(it.product([GREY, TAN, GREEN], repeat=5))

RESPS = []
GUESSES = []


def find_words(conditions, guess, data):
    for i, cond in enumerate(conditions):
        v, ch = cond, guess[i]
        if v == GREY:
            data = [x for x in data if ch not in x]
        elif v == TAN:
            data = [x for x in data if (ch in x and ch != x[i])]
        elif v == GREEN:
            data = [x for x in data if ch == x[i]]
    return data


def info(prob):
    return math.log2(1/prob) if prob > 0 else 0


def exp(word, data):
    exp_val = 0
    for val in vals:
        match = find_words(val, word, data)
        prob = len(match) / WORDS_SIZE
        exp_val += info(prob) * prob

    # print(f'{word}:\t{exp_val}')
    return exp_val


def find_st_word(data):
    best_words = [(word, exp(word, data)) for word in data]
    return list(sorted(best_words, key=lambda x: x[1], reverse=True))


def print_colored(resp, guess):
    for i, ch in enumerate(guess):
        cprint(ch, 'grey', COLORS[resp[i]], end='')


def play(resp, guess, data):
    GUESSES.append(guess)
    RESPS.append(resp)
    match = find_words(resp, guess, data)

    for i in range(len(GUESSES)):
        print_colored(RESPS[i], GUESSES[i])
        print()

    print(f'\nInformation:\t{info(len(match)/WORDS_SIZE)}')
    print(f'Entropy:\t{exp(guess, data)}')
    print(f'Uncertainty:\t{math.log2(len(match))}')
    print(len(match), end=': ')

    nexts = 5 if len(match) > 5 else len(match)-1
    for i in range(nexts):
        print(match[i], end=', ')
    print(match[nexts])

    return match


def eval(key, guess):
    resp = []
    for i, ch in enumerate(guess):
        color = TAN
        if key[i] == ch:
            color = GREEN
        if ch not in key:
            color = GREY
        resp.append(color)

    return resp


def build_puzzle(data):
    KEY = P_WORDS[random.randrange(0, P_WORDS_SIZE)]
    poss, guess = WORDS, ""
    while guess != KEY:
        guess = input('\nWord Guess: ')
        resp = eval(KEY, guess)
        poss = play(resp, guess, poss)
    print_colored(eval(KEY, guess), guess)

    return len(GUESSES)


def main():
    # for word in find_st_word(WORDS):
    #     print(f'{word[0]}:\t{word[1]}')
    # find_st_word(WORDS)
    # word = 'tares'
    # print(word + ":\t", exp(word, WORDS))
    while True:
        RESPS.clear()
        GUESSES.clear()
        guesses = build_puzzle(WORDS)
        print('\n------------------------------')
        print(f'--------- {guesses} ATTEMPTS ---------')
        print('------------------------------')


if __name__ == '__main__':
    main()
