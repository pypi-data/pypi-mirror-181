from sourpea.primitives import Factor, DerivedLevel, DerivationWindow, Block, TransitionDerivationWindow, Level, Exclude
import pandas as pd

PATHS = [f'kaneEtAl/ckm_2_back_{l}.txt' for l in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
PATHS_THREE = [f'kaneEtAl/ckm_3_back_{l}.txt' for l in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]



def test_sequence_two_back(trial_sequence, name):
    letter = Factor('letter', ['b', 'f', 'm', 'q', 'k', 'x', 'r', 'h'])

    def is_target(letters):
        return letters[0] == letters[2]

    def is_not_target(letters):
        return not is_target(letters)

    one_t = DerivedLevel('1', DerivationWindow(is_target, [letter], 3), 8 / 48)
    two_t = DerivedLevel('2', DerivationWindow(is_not_target, [letter], 3), 40 / 48)

    target = Factor('target', [one_t, two_t])

    def is_one_back(letters):
        return letters[0] == letters[1]

    def is_not_one_back(letters):
        return not is_one_back(letters)

    two_o = DerivedLevel('2', DerivationWindow(is_one_back, [letter], 2), 8 / 48)
    one_o = DerivedLevel('1', DerivationWindow(is_not_one_back, [letter], 2), 40 / 48)

    one_back = Factor('one_back', [one_o, two_o])

    def is_three_back(letters):
        return letters[0] == letters[3]

    def is_not_three_back(letters):
        return not is_three_back(letters)

    one_three = DerivedLevel('1', DerivationWindow(is_three_back, [letter], 4), 1 / 48)
    zero_three = DerivedLevel('0', DerivationWindow(is_not_three_back, [letter], 4), 1)

    three_back = Factor('three_back', [one_three, zero_three])

    def is_control_target(letters):
        return is_target(letters) and letters[2] != letters[1]

    def is_experimental_target(letters):
        return is_target(letters) and letters[2] == letters[1]

    def is_control_foil(letters):
        return is_not_target(letters) and letters[2] != letters[1]

    def is_experimental_foil(letters):
        return is_not_target(letters) and letters[2] == letters[1]

    one_one_0 = DerivedLevel('1/1/0', DerivationWindow(is_control_target, [letter], 3), 6 / 48)
    one_two_0 = DerivedLevel('1/2/0', DerivationWindow(is_experimental_target, [letter], 3), 2 / 48)
    two_one_0 = DerivedLevel('2/1/0', DerivationWindow(is_control_foil, [letter], 3), 34 / 48)
    two_two_0 = DerivedLevel('2/2/0', DerivationWindow(is_experimental_foil, [letter], 3), 6 / 48)

    condi = Factor('condi', [one_one_0, one_two_0, two_one_0, two_two_0])

    block = Block(design=[letter, target, one_back], crossing=[letter, target])
    test = block.test(trial_sequence)

    block_2 = Block(design=[letter, one_back], crossing=[letter, one_back])
    test_2 = block_2.test(trial_sequence)

    block_3 = Block(design=[letter, condi], crossing=[letter, condi])
    test_3 = block_3.test(trial_sequence)

    block_4 = Block(design=[letter, three_back], constraints=[Exclude(three_back, '1')], crossing=[letter])
    test_4 = block_4.test(trial_sequence)

    block_5 = Block(design=[letter, condi], crossing=[condi])
    test_5 = block_5.test(trial_sequence)


    print(name)
    print(test)
    print(test_2)
    print(test_3)
    print(test_4)
    print(test_5)
    print('\n')


def sequence_two_txt(path):
    f = open(path)
    trials = []
    for line in f:
        if line[-8] != '\\':
            trials.append(
                {'letter': line[-8],
                 'target': line[-6].replace('\n', '').replace('\\', '/'),
                 'one_back': line[-4].replace('\n', '').replace('\\', '/'),
                 'three_back': line[-2].replace('\n', '').replace('\\', '/'),
                 'condi': line[-6:].replace('\n', '').replace('\\', '/')})
        else:
            trials.append({
                'letter': line[-7],
                'target': line[-5].replace('\n', '').replace('\\', '/'),
                'one_back': line[-3].replace('\n', '').replace('\\', '/'),
                'three_back': line[-1].replace('\n', '').replace('\\', '/'),
                'condi': line[-5:].replace('\n', '').replace('\\', '/')})
    return trials


def sequence_two_csv(path):
    df = pd.read_csv(path)
    letters = list(df['letter'])
    condi = list(df['condi'])
    sequence = []
    for l, c in zip(letters, condi):
        c = str(c)
        if not c == 'nan':
            sequence.append({'letter': l, 'target': c[0], 'one_back': c[2], 'three_back': c[-1], 'condi': c})
    return sequence


def sequence_three(path):
    f = open(path)
    trials = []
    for line in f:
        if line[-8] != '\\':
            trials.append(
                {'letter': line[-8],
                 'target': line[-6].replace('\n', '').replace('\\', '/'),
                 'one_or_two': line[-4].replace('\n', '').replace('\\', '/'),
                 'lure': line[-2].replace('\n', '').replace('\\', '/'),
                 'condi': line[-6:].replace('\n', '').replace('\\', '/')})
        else:
            trials.append({
                'letter': line[-7],
                'target': line[-5].replace('\n', '').replace('\\', '/'),
                'one_or_two': line[-3].replace('\n', '').replace('\\', '/'),
                'lure': line[-1].replace('\n', '').replace('\\', '/'),
                'condi': line[-5:].replace('\n', '').replace('\\', '/')})
    return trials


def test_three_back(PATH):
    trial_sequence = sequence_three(PATH)

    letter = Factor('letter', ['b', 'f', 'm', 'q', 'k', 'x', 'r', 'h'])

    def is_target(letters):
        return letters[0] == letters[3]

    def is_not_target(letters):
        return not is_target(letters)

    one_t = DerivedLevel('1', DerivationWindow(is_target, [letter], 4), 8 / 48)
    two_t = DerivedLevel('2', DerivationWindow(is_not_target, [letter], 4), 40 / 48)

    target = Factor('target', [one_t, two_t])

    def is_one_or_two(letters):
        return letters[1] == letters[2] or letters[0] == letters[2]

    def is_not_one_or_two(letters):
        return not is_one_or_two(letters)

    two_o = DerivedLevel('2', DerivationWindow(is_one_or_two, [letter], 3), 9 / 48)
    one_o = DerivedLevel('1', DerivationWindow(is_not_one_or_two, [letter], 3), 39 / 48)

    one_or_two = Factor('one_or_two', [one_o, two_o])

    def is_lure_one(letters):
        return not letters[0] == letters[3] and letters[3] == letters[2]

    def is_lure_two(letters):
        return not letters[0] == letters[3] and letters[3] == letters[1]

    def is_not_lure(letters):
        return not (is_lure_one(letters) or is_lure_two(letters))

    one_lure = DerivedLevel('1', DerivationWindow(is_lure_one, [letter], 4), 1 / 48)
    two_lure = DerivedLevel('2', DerivationWindow(is_lure_two, [letter], 4), 6 / 48)
    zero_lure = DerivedLevel('0', DerivationWindow(is_not_lure, [letter], 4), 41 / 48)

    lure = Factor('lure', [one_lure, two_lure, zero_lure])

    def is_control_target(letters):
        return letters[0] == letters[3] and letters[2] != letters[3] and letters[1] != letters[3]

    def is_experimental_target(letters):
        return letters[0] == letters[3] and letters[2] == letters[3]

    def is_control_foil(letters):
        return letters[0] != letters[3] and letters[1] != letters[3] and letters[2] != letters[3]

    def is_experimental_two_foil(letters):
        return letters[0] != letters[3] and letters[1] == letters[3]

    def is_experimental_one_foil(letters):
        return letters[0] != letters[3] and letters[2] == letters[3]

    one_one_0 = DerivedLevel('1/1/0', DerivationWindow(is_control_target, [letter], 4), 6 / 48)
    one_two_0 = DerivedLevel('1/2/0', DerivationWindow(is_experimental_target, [letter], 4), 2 / 48)
    two_one_0 = DerivedLevel('2/1/0', DerivationWindow(is_control_foil, [letter], 4), 33 / 48)
    two_two_two = DerivedLevel('2/2/2', DerivationWindow(is_experimental_two_foil, [letter], 4), 6 / 48)
    two_two_one = DerivedLevel('2/2/1', DerivationWindow(is_experimental_one_foil, [letter], 4), 1 / 48)

    condi = Factor('condi', [one_one_0, one_two_0, two_one_0, two_two_two, two_two_one])

    block = Block(design=[letter, target, one_or_two], crossing=[letter, target])
    test = block.test(trial_sequence)

    block_2 = Block(design=[letter, one_or_two], crossing=[one_or_two])
    test_2 = block_2.test(trial_sequence)

    block_3 = Block(design=[letter, lure], crossing=[lure])
    test_3 = block_3.test(trial_sequence)

    block_4 = Block(design=[letter, condi], crossing=[condi])
    test_4 = block_4.test(trial_sequence)

    print(PATH)
    print(test)
    print(test_2)
    print(test_3)
    print(test_4)
    print('\n')


def test_two_back_real(PATH):
    trial_sequence = sequence_two_txt(PATH)
    test_sequence_two_back(trial_sequence, PATH)


def test_two_back_csv(PATH):
    trial_sequence = sequence_two_csv(PATH)
    test_sequence_two_back(trial_sequence, PATH)


for p in PATHS:
    test_two_back_real(p)

# for p in PATHS_THREE:
#    test_three_back(p)

paths = [f'sweetKaneEtAl/test_{str(i)}_0.csv' for i in range(1,7)]
for p in paths:
    print(p)
    test_two_back_csv(p)
