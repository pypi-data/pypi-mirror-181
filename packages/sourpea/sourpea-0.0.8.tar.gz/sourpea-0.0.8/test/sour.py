from sourpea.primitives import Factor, DerivedLevel, DerivationWindow, Block, TransitionDerivationWindow, Level, Exclude

sequence = [
    {'letter': 'b', 'target': None},
    {'letter': 'f', 'target': None},
    {'letter': 'b', 'target': '1'},
    {'letter': 'b', 'target': '2'}
]

letter = Factor('letter', ['b', 'f', 'm', 'q', 'k', 'x', 'r', 'h'])

def is_target(letters):
    return letters[0] == letters[-2]


def is_not_target(letters):
    return not is_target(letters)

one_t = DerivedLevel('1', DerivationWindow(is_target, [letter], 3), 8 / 48)
two_t = DerivedLevel('2', DerivationWindow(is_not_target, [letter], 3), 40 / 48)

target = Factor('target', [one_t, two_t])

block_4 = Block(design=[letter, target], crossing=[target])
test_4 = block_4.test(sequence)

print(test_4['pValue'], test_4['levels'])
