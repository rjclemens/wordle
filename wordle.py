import math
import itertools as it
import random
from termcolor import cprint
import json

with open('data/words.txt') as file:
    WORDS = file.read().split('\n')

with open('data/possible_words.txt') as file:
    P_WORDS = file.read().split('\n')

with open('data/words_freqs.txt') as file:
    FREQS = file.read().split(',')

FREQ_DICT = dict()

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


def exp(word, data, size=WORDS_SIZE):
    exp_val = 0
    for val in vals:
        match = find_words(val, word, data)
        prob = len(match) / size
        exp_val += info(prob) * prob

    # print(f'{word}:\t{exp_val}')
    return exp_val


def sigmoid(x):
    try:
        # centered based on index
        return 1 / (1 + math.exp(-(-x+2500)/500))
    except:
        return 0


def freq(FREQS):
    # parse json-formatted word freq text file
    FREQS = [(x.split(':')[0][2:7], float(x.split(':')[1][1:])) for x in FREQS]
    FREQS = list(sorted(FREQS, key=lambda x: x[1], reverse=True))
    for i, elem in enumerate(FREQS):
        FREQ_DICT[elem[0]] = sigmoid(i)


def find_best_word(data, guesses):
    best_words = [(word, exp(word, data, len(data)), FREQ_DICT.get(word))
                  for word in data]
    return list(sorted(best_words, key=lambda x: x[1]+(guesses/2)*x[2], reverse=True))


def print_colored(resp, guess):
    for i, ch in enumerate(guess):
        cprint(ch, 'grey', COLORS[resp[i]], end='')


def play(resp, guess, data):
    GUESSES.append(guess)
    RESPS.append(resp)
    guess_count = len(GUESSES)
    match = find_words(resp, guess, data)

    for i in range(guess_count):
        print_colored(RESPS[i], GUESSES[i])
        print()

    print(f'\nInformation:\t{info(len(match)/WORDS_SIZE)}')
    print(f'Entropy:\t{exp(guess, data)}')
    print(f'Uncertainty:\t{math.log2(len(match)) if len(match) > 0 else 0}')
    print(len(match))

    best_words = find_best_word(match, guess_count)

    nexts = 5 if len(best_words) > 5 else len(best_words)
    for i in range(nexts):
        print(f'{best_words[i][0]}:\t{best_words[i][1]}\t{best_words[i][2]}')

    return match, best_words[0][0]


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
    print("KEY:", KEY.upper())
    while guess != KEY:
        guess = input('\nWord Guess: ')
        resp = eval(KEY, guess)
        poss, _ = play(resp, guess, poss)
    print_colored(eval(KEY, guess), guess)

    return len(GUESSES)


def run(iter):
    freq(FREQS)
    attempts = []
    for i in range(iter):
        RESPS.clear()
        GUESSES.clear()
        KEY = P_WORDS[random.randrange(0, P_WORDS_SIZE)]
        poss, guess = WORDS, "tares"
        while guess != KEY:
            resp = eval(KEY, guess)
            poss, guess = play(resp, guess, poss)
        print_colored(eval(KEY, guess), guess)

        print('\n------------------------------')
        print(f'--------- {len(GUESSES)+1} ATTEMPTS ---------')
        print('------------------------------')

        attempts.append((KEY, len(GUESSES)+1))

    return attempts


def main():
    # for word in find_best_word(WORDS):
    #     print(f'{word[0]}:\t{word[1]}')
    # find_best_word(WORDS)
    # word = 'tares'
    # print(word + ":\t", exp(word, WORDS))
    # while True:
    #     RESPS.clear()
    #     GUESSES.clear()
    #     guesses = build_puzzle(WORDS)
    #     print('\n------------------------------')
    #     print(f'--------- {guesses} ATTEMPTS ---------')
    #     print('------------------------------')

    # freq(FREQS)
    # print(dict(sorted(FREQ_DICT.items(), key=lambda x: x[1])))

    stats = run(200)
    avg = sum([x[1] for x in stats])/len(stats)
    print(f'Average: {avg}')

    stats = list(sorted(stats, key=lambda x: x[1], reverse=True))
    for x in stats:
        print(f'{x[0]}: {x[1]}')


if __name__ == '__main__':
    main()
