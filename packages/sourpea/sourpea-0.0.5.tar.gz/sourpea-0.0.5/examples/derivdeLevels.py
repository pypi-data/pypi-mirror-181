from sourpea.primitives import DerivedLevel, Level, Factor, Block, WithinTrialDerivationWindow, \
    TransitionDerivationWindow

# valid test sequence
test_sequence_1 = [
    {'word': 'red', 'color': 'red', 'congruency': 'con'},
    {'word': 'red', 'color': 'green', 'congruency': 'inc'},
    {'word': 'green', 'color': 'red', 'congruency': 'inc'},
    {'word': 'green', 'color': 'green', 'congruency': 'con'},
]

# invalid test sequence: derived level mixup
test_sequence_2 = [
    {'word': 'red', 'color': 'red', 'congruency': 'inc'},
    {'word': 'red', 'color': 'green', 'congruency': 'con'},
    {'word': 'green', 'color': 'red', 'congruency': 'con'},
    {'word': 'green', 'color': 'green', 'congruency': 'inc'},
]

# invalid test sequence: not counterbalanced
test_sequence_3 = [
    {'word': 'red', 'color': 'green', 'congruency': 'inc'},
    {'word': 'red', 'color': 'green', 'congruency': 'inc'},
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

congruency_2 = Factor('congruency', ['con', 'inc'])

block = Block(design=[word, color, congruency], crossing=[word, congruency])
test_1 = block.test(test_sequence_1)
test_2 = block.test(test_sequence_2)
test_3 = block.test(test_sequence_3)

print(test_1['pValue'], test_1['levels'])
print(test_2['pValue'], test_2['levels'])
print(test_3['pValue'], test_3['levels'])

test_sequence_4 = [
    {'task': 'color naming', 'congruency': 'congruent', 'transition': None},
    {'task': 'color naming', 'congruency': 'congruent', 'transition': 'full repetition'},
    {'task': 'word naming', 'congruency': 'congruent', 'transition': 'half repetition'},
    {'task': 'color naming', 'congruency': 'incongruent', 'transition': 'switch'}
]

test_sequence_5 = [
    {'task': 'color naming', 'congruency': 'congruent', 'transition': None},
    {'task': 'color naming', 'congruency': 'congruent', 'transition': 'full repetition'},
    {'task': 'color naming', 'congruency': 'incongruent', 'transition': 'half repetition'},
    {'task': 'word naming', 'congruency': 'congruent', 'transition': 'switch'},
    {'task': 'word naming', 'congruency': 'congruent', 'transition': 'full repetition'},
    {'task': 'word naming', 'congruency': 'incongruent', 'transition': 'half repetition'},
    {'task': 'color naming', 'congruency': 'congruent', 'transition': 'switch'}
]

test_sequence_6 = [
    {'task': 'color naming', 'congruency': 'congruent', 'transition': None},
    {'task': 'color naming', 'congruency': 'congruent', 'transition': 'full repetition'},
    {'task': 'color naming', 'congruency': 'incongruent', 'transition': 'half repetition'},
    {'task': 'word naming', 'congruency': 'congruent', 'transition': 'switch'},
    {'task': 'word naming', 'congruency': 'congruent', 'transition': 'full repetition'},
    {'task': 'word naming', 'congruency': 'incongruent', 'transition': 'half repetition'},
    {'task': 'color naming', 'congruency': 'incongruent', 'transition': 'half repetition'}
]

task = Factor('task', ['color naming', 'word naming'])
congruency = Factor('congruency', ['congruent', 'incongruent'])


def is_full_repetition(t, c):
    return t[0] == t[1] and c[0] == c[1]


def is_switch(t, c):
    return t[0] != t[1] and c[0] != c[1]


def is_half_repetition(t, c):
    return not (is_full_repetition(t, c) or is_switch(t, c))


full_repetition = DerivedLevel('full repetition',
                               TransitionDerivationWindow(predicate=is_full_repetition, factors=[task, congruency]))
switch = DerivedLevel('switch',
                      TransitionDerivationWindow(predicate=is_switch, factors=[task, congruency]))
half_repetition = DerivedLevel('half repetition',
                               TransitionDerivationWindow(predicate=is_half_repetition, factors=[task, congruency]))

transition = Factor('transition', [full_repetition, switch, half_repetition])

block_4 = Block(design=[task, congruency, transition], crossing=[transition])
test_4 = block_4.test(test_sequence_4)

print(test_4['pValue'], test_4['levels'])

block_5 = Block(design=[task, congruency, transition], crossing=[task, transition])
test_5 = block_5.test(test_sequence_5)

print(test_5['pValue'], test_5['levels'])

block_6 = Block(design=[task, congruency, transition], crossing=[task, transition])
test_6 = block_6.test(test_sequence_6)

print(test_6['pValue'], test_6['levels'])
