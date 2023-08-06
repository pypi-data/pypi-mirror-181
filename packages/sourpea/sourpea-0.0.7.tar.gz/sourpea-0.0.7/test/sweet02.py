from sweetpea import Factor, DerivedLevel, Window, MultiCrossBlock, synthesize_trials, Exclude, MinimumTrials, \
    CrossBlock, save_experiments_csv


def create_two_back():
    letter = Factor('letter', ['b', 'f', 'm', 'q', 'k', 'x', 'r', 'h'])

    def is_target(letters):
        if not letters:
            return False
        return letters[-2] == letters[0]

    def is_not_target(letters):
        if not letters:
            return True
        return not is_target(letters)

    one_t = DerivedLevel('1', Window(is_target, [letter], width=3, stride=1, start=0), 1)
    two_t = DerivedLevel('2', Window(is_not_target, [letter], width=3, stride=1, start=0), 5)

    target = Factor('target', [one_t, two_t])

    # def is_one_back(letters):
    #     if letters is None:
    #         return False
    #     return letters[-1] == letters[0]
    #
    # def is_not_one_back(letters):
    #     return not is_one_back(letters)
    #
    # two_o = DerivedLevel('2', Window(is_one_back, [letter], width=2, stride=1, start=1), 1)
    # one_o = DerivedLevel('1', Window(is_not_one_back, [letter], width=2, stride=1, start=1), 5)
    #
    # one_back = Factor('one_back', [one_o, two_o])
    #
    # def is_three_back(letters):
    #     if letters is None:
    #         return False
    #     return letters[-3] == letters[0]
    #
    # def is_not_three_back(letters):
    #     return not is_three_back(letters)
    #
    # one_three = DerivedLevel('1', Window(is_three_back, [letter], width=4, stride=1, start=1))
    # zero_three = DerivedLevel('0', Window(is_not_three_back, [letter], width=4, stride=1, start=1))
    #
    # three_back = Factor('three_back', [one_three, zero_three])
    #
    # def is_control_target(letters):
    #     if letters is None:
    #         return False
    #     return is_target(letters) and letters[0] != letters[-1]
    #
    # def is_experimental_target(letters):
    #     if letters is None:
    #         return False;
    #     return is_target(letters) and letters[0] == letters[-1]
    #
    # def is_control_foil(letters):
    #     if letters is None:
    #         return False
    #     return is_not_target(letters) and letters[0] != letters[-1]
    #
    # def is_experimental_foil(letters):
    #     if letters is None:
    #         return True
    #     return is_not_target(letters) and letters[0] == letters[-1]
    #
    # one_one_0 = DerivedLevel('1/1/0', Window(is_control_target, [letter], width=3, stride=1, start=1), 3)
    # one_two_0 = DerivedLevel('1/2/0', Window(is_experimental_target, [letter], width=3, stride=1, start=1), 1)
    # two_one_0 = DerivedLevel('2/1/0', Window(is_control_foil, [letter], width=3, stride=1, start=1), 17)
    # two_two_0 = DerivedLevel('2/2/0', Window(is_experimental_foil, [letter], width=3, stride=1, start=1), 3)
    #
    # condi = Factor('condi', [one_one_0, one_two_0, two_one_0, two_two_0])

    block = CrossBlock(design=[letter, target],
                            constraints=[MinimumTrials(48)],
                            crossing=[letter, target])

    experiment = synthesize_trials(block, 1)

    save_experiments_csv(block, experiment, "sweetKaneEtAl/test")


create_two_back()
