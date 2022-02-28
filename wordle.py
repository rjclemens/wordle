import math
import itertools as it

GREY = 0
TAN = 1
GREEN = 2

with open('words.txt') as word_file:
    DATA = word_file.read().split(',')

DATA_SIZE = len(DATA)
print(DATA_SIZE)

vals = list(it.product([GREY, TAN, GREEN], repeat=5))


def find_words(conditions, guess, data):
    for i, cond in enumerate(conditions):
        v, ch = cond, guess[i]
        if v == GREY:
            data = [x for x in data if ch not in x]
        elif v == TAN:
            data = [x for x in data if ch in x]
        elif v == GREEN:
            data = [x for x in data if ch == x[i]]

    # print(conditions, guess, len(data))
    # print("-----------")
    return data


def info(data):
    try:
        return math.log2(DATA_SIZE / len(data))
    except:
        return 0


def exp(word, data):
    exp_val = 0
    for val in vals:
        match = find_words(val, word, data)
        exp_val += info(match) * (len(match) / DATA_SIZE)

    print(f'{word}:\t{exp_val}')
    return exp_val


def find_st_word(data):
    best_words = []
    # best_words = [(word, exp(word, data)) for word in data]
    for word in data:
        best_words.append((word, exp(word, data)))

    return list(sorted(best_words, key=lambda x: x[1]))


def main():
    for word in find_st_word(DATA):
        print(f'{word[0]}:\t{word[1]}')


if __name__ == '__main__':
    main()
