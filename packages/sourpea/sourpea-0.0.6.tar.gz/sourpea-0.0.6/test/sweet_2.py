from sweetpea import Factor, DerivedLevel, DerivationWindow, MultiCrossBlock, synthesize_trials, Exclude, MinimumTrials, \
    CrossBlock, save_experiments_csv


def create_two_back():
    letter = Factor('letter', ['b', 'f', 'm', 'q', 'k', 'x', 'r', 'h'])

    def is_target(letters):
        return letters[0] == letters[2]

    def is_not_target(letters):
        return not is_target(letters)

    one_t = DerivedLevel('1', DerivationWindow(is_target, [letter], 3, 1), 1)
    two_t = DerivedLevel('2', DerivationWindow(is_not_target, [letter], 3, 1), 5)

    target = Factor('target', [one_t, two_t])

    def is_one_back(letters):
        return letters[0] == letters[1]

    def is_not_one_back(letters):
        return not is_one_back(letters)

    two_o = DerivedLevel('2', DerivationWindow(is_one_back, [letter], 2, 1), 1)
    one_o = DerivedLevel('1', DerivationWindow(is_not_one_back, [letter], 2, 1), 5)

    one_back = Factor('one_back', [one_o, two_o])

    def is_one_but_not_two(letters):
        return letters[0] != letters[1] and letters[1] == letters[2]
    def is_not_one_but_not_two(letters):
        return not is_one_but_not_two(letters)

    obnt_one = DerivedLevel('1', DerivationWindow(is_one_but_not_two, [letter], 3, 1),1)
    obnt_two = DerivedLevel('2', DerivationWindow(is_not_one_but_not_two, [letter], 3, 1),5)
    obnt = Factor('obnt', [obnt_one, obnt_two])

    def is_three_back(letters):
        return letters[0] == letters[3]

    def is_not_three_back(letters):
        return not is_three_back(letters)

    one_three = DerivedLevel('1', DerivationWindow(is_three_back, [letter], 4, 1))
    zero_three = DerivedLevel('0', DerivationWindow(is_not_three_back, [letter], 4, 1))

    three_back = Factor('three_back', [one_three, zero_three])

    def is_control_target(letters):
        return is_target(letters) and letters[2] != letters[1]

    def is_experimental_target(letters):
        return is_target(letters) and letters[2] == letters[1]

    def is_control_foil(letters):
        return is_not_target(letters) and letters[2] != letters[1]

    def is_experimental_foil(letters):
        return is_not_target(letters) and letters[2] == letters[1]

    one_one_0 = DerivedLevel('1/1/0', DerivationWindow(is_control_target, [letter], 3, 1), 3)
    one_two_0 = DerivedLevel('1/2/0', DerivationWindow(is_experimental_target, [letter], 3, 1), 1)
    two_one_0 = DerivedLevel('2/1/0', DerivationWindow(is_control_foil, [letter], 3, 1), 17)
    two_two_0 = DerivedLevel('2/2/0', DerivationWindow(is_experimental_foil, [letter], 3, 1), 3)

    condi = Factor('condi', [one_one_0, one_two_0, two_one_0, two_two_0])

    block = MultiCrossBlock(design=[letter, target, one_back, condi, three_back, obnt],
                            constraints=[Exclude(three_back, '1'), MinimumTrials(48)],
                            crossings=[[letter, target], [letter, obnt],[condi]])

    experiment = synthesize_trials(block, 1)

    print(experiment)
    save_experiments_csv(block, experiment, "sweetKaneEtAl/test_7")


create_two_back()
