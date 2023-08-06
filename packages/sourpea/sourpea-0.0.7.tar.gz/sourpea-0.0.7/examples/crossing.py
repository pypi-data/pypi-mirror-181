from sourpea.primitives import Level, Factor, Block

# counterbalance 1
# sequence to test on
test_sequence_1 = [
    {'word': 'red', 'color': 'red'},
    {'word': 'green', 'color': 'red'},
    {'word': 'red', 'color': 'green'},
    {'word': 'green', 'color': 'green'},
]

# defining the factors
word = Factor('word', ['red', 'green'])
color = Factor('color', ['red', 'green'])

# defining the design (counterbalancing)
block_1 = Block(design=[word, color], crossing=[word, color])

# getting the results
test_1 = block_1.test(test_sequence_1)
print('sequence1, design1: ', test_1['pValue'], test_1['levels'])

# counterbalance with weighted factors
# sequence to test on
test_sequence_2 = [
    {'word': 'red', 'color': 'red'},
    {'word': 'green', 'color': 'red'},
    {'word': 'red', 'color': 'red'},
    {'word': 'green', 'color': 'green'},
    {'word': 'red', 'color': 'green'},
    {'word': 'red', 'color': 'green'}
]

# defining the factors
word_2 = Factor('word', [Level('red', 2), 'green'])
color_2 = Factor('color', ['red', 'green'])

# defining the design
block_2 = Block(design=[color_2, word_2], crossing=[word_2, color_2])

# getting the result
test_2 = block_2.test(test_sequence_2)
print('sequence2, design2: ', test_2['pValue'], test_2['levels'])

# counterbalance with more weights
# sequence to test on
test_sequence_3 = [
    {'word': 'red', 'color': 'green'},
    {'word': 'red', 'color': 'green'},
    {'word': 'red', 'color': 'green'},
    {'word': 'red', 'color': 'green'},
    {'word': 'red', 'color': 'green'},
    {'word': 'red', 'color': 'green'},
    {'word': 'red', 'color': 'red'},
    {'word': 'red', 'color': 'red'},
    {'word': 'red', 'color': 'red'},
    {'word': 'red', 'color': 'red'},
    {'word': 'green', 'color': 'green'},
    {'word': 'green', 'color': 'green'},
    {'word': 'green', 'color': 'green'},
    {'word': 'green', 'color': 'red'},
    {'word': 'green', 'color': 'red'},
]

# defining factors
word_3 = Factor('word', [Level('red', 2), Level('green', 1)])
color_3 = Factor('color', [Level('red', 2), Level('green', 3)])

# defining design
block_3 = Block(design=[word_3, color_3], crossing=[word_3, color_3])

# getting the results
test_3 = block_3.test(test_sequence_3)
print('sequence3, design3: ', test_3['pValue'], test_3['levels'])

# cross validating (this should result in lower p-values)
test_4 = block_1.test(test_sequence_2)
print('sequence2, design1: ', test_4['pValue'], test_4['levels'])

test_5 = block_2.test(test_sequence_1)
print('sequence1, design2: ', test_5['pValue'], test_5['levels'])
