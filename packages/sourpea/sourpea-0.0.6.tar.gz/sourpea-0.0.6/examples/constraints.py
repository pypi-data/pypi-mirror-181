from sourpea.primitives import Factor, Level, Block, MinimumTrials, AtMostKInARow, AtLeastKInARow, ExactlyKInARow, \
    ExactlyK

test_sequence = [
    {'direction': 'up', 'orientation': 'down', 'congruency': 'incongruent'},
    {'direction': 'down', 'orientation': 'down', 'congruency': 'congruent'},
    {'direction': 'up', 'orientation': 'up', 'congruency': 'incongruent'},
    {'direction': 'down', 'orientation': 'up', 'congruency': 'congruent'},
]

test_sequence_2 = [
    {'direction': 'up', 'orientation': 'down', 'congruency': 'incongruent'},
    {'direction': 'up', 'orientation': 'up', 'congruency': 'congruent'},
    {'direction': 'up', 'orientation': 'up', 'congruency': 'incongruent'},
    {'direction': 'down', 'orientation': 'up', 'congruency': 'congruent'},
]

direction = Factor(name='direction', initial_levels=['up', 'down'])
orientation = Factor(name='orientation', initial_levels=['up', 'down'])

minimum_trials = MinimumTrials(4)
minimum_trials_2 = MinimumTrials(8)
atMostKInARow = AtMostKInARow(2, (direction, ['up']))
atMostKInARow_2 = AtMostKInARow(2, direction)
atLeastKInARow = AtLeastKInARow(2, orientation)
atLeastKInARow_2 = AtLeastKInARow(2, (orientation, 'up'))
exactlyKInARow = ExactlyKInARow(2, orientation)
exactlyKInARow_2 = ExactlyKInARow(3, (direction, Level('up')))
exactlyK = ExactlyK(3, (direction, 'up'))

block = Block(constraints=[minimum_trials, atMostKInARow, atLeastKInARow, exactlyKInARow, exactlyK])
block_2 = Block(constraints=[minimum_trials_2, atMostKInARow_2, atLeastKInARow_2, exactlyKInARow_2, exactlyK])

test = block.test(test_sequence)
test_2 = block.test(test_sequence_2)
test_3 = block_2.test(test_sequence)
test_4 = block_2.test(test_sequence_2)

print(test)
print(test_2)
print(test_3)
print(test_4)
