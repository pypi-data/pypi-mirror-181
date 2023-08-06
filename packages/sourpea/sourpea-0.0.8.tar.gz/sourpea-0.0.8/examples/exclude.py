from sourpea.primitives import DerivedLevel, Level, Factor, Block, WithinTrialDerivationWindow, \
    TransitionDerivationWindow, Exclude

# valid test sequence
test_sequence_1 = [
    {'word': 'red', 'color': 'red', 'congruency': 'con'},
    {'word': 'green', 'color': 'green', 'congruency': 'con'},
]

# invalid test sequence: derived level mixup
test_sequence_2 = [
    {'word': 'red', 'color': 'red', 'congruency': 'inc'},
    {'word': 'red', 'color': 'green', 'congruency': 'inc'},
    {'word': 'green', 'color': 'red', 'congruency': 'con'},
    {'word': 'green', 'color': 'green', 'congruency': 'con'},
]

# valid test
test_sequence_3 = [
    {'word': 'red', 'color': 'red', 'congruency': 'con'},
    {'word': 'red', 'color': 'red', 'congruency': 'con'},
    {'word': 'green', 'color': 'green', 'congruency': 'con'},
    {'word': 'green', 'color': 'green', 'congruency': 'con'},
]

word = Factor('word', ['red', 'green'])
color = Factor('color', ['red', 'green'])


def is_con(w, c):
    return w == c


def is_inc(w, c):
    return not is_con(w, c)


congruent = DerivedLevel('con', window=WithinTrialDerivationWindow(predicate=is_con, factors=[word, color]))
incongruent = DerivedLevel('inc', window=WithinTrialDerivationWindow(predicate=is_inc, factors=[word, color]))

congruency = Factor('congruency', [congruent, incongruent])

exclude = Exclude('congruency', 'inc')

block = Block(design=[word, color, congruency], crossing=[word, congruency], constraints=[exclude])
test_1 = block.test(test_sequence_1)
test_2 = block.test(test_sequence_2)
test_3 = block.test(test_sequence_3)

print(test_1['pValue'], test_1['levels'])
print(test_2['pValue'], test_2['levels'])
print(test_3['pValue'], test_3['levels'])
