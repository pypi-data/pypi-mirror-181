from __future__ import annotations
from typing import Callable, List, Tuple
from scipy.stats import chisquare


class Level:
    """
    A discrete value that a :class:`.Factor` can hold.
    """
    name: str
    weight: float = 1

    def __init__(self, name: str, weight: float = 1):
        self.name = name
        self.weight = weight


class DerivedLevel(Level):
    window: DerivationWindow

    def __init__(self, name: str, window: DerivationWindow, weight: float = 1):
        super().__init__(name, weight)
        self.window = window


class Factor:
    """An independent variable in a factorial experiment. Factors are composed
    of :class:`Levels <.Level>` and come in two flavors:
    """
    name: str
    levels: List[Level]

    def __init__(self, name: str, initial_levels: list):
        self.name = name
        self.levels = []
        for level in initial_levels:
            if type(level) == str:
                self.levels.append(Level(level))
            elif isinstance(level, Level):
                self.levels.append(level)


class DerivationWindow:
    predicate: Callable
    factors: List[Factor]
    width: int

    def __init__(self, predicate: Callable, factors: List[Factor], width: int = 1):
        self.predicate = predicate
        self.factors = factors
        self.width = width


class WithinTrialDerivationWindow(DerivationWindow):

    def __init__(self, predicate: Callable, factors: List[Factor]):
        super().__init__(predicate, factors)
        self.width = 1


# Aliases
WithinTrial = WithinTrialDerivationWindow


class TransitionDerivationWindow(DerivationWindow):

    def __init__(self, predicate: Callable, factors: List[Factor]):
        super().__init__(predicate, factors)
        self.width = 2


# Aliases
Transition = TransitionDerivationWindow


class Constraint:

    def __init__(self):
        pass

    def test(self, sequence: List):
        return True


class Exclude(Constraint):
    factor: str
    level: str

    def __init__(self, factor: Factor, level: Level):
        if isinstance(factor, Factor):
            self.factor = factor.name
        else:
            self.factor = factor
        if isinstance(level, Level):
            self.level = level.name
        else:
            self.level = level

    def test(self, sequence: List):
        for trial in sequence:
            if trial[self.factor] == self.level:
                return False
        return True


class _NumberConstraint:
    trials: int

    def __init__(self, trials: int):
        super().__init__()
        self.trials = trials


class MinimumTrials(_NumberConstraint):

    def test(self, sequence: List):
        return len(sequence) >= self.trials


class _KConstraint(_NumberConstraint):
    factor: Factor
    levels: List[Level]

    def __init__(self, trials: int, level: Tuple[Factor, List[Level]]):
        super().__init__(trials)
        if isinstance(level, Factor):
            self.factor = level
            self.levels = level.levels
        if isinstance(level, Tuple):
            self.factor = level[0]
            if isinstance(level[1], List):
                self.levels = level[1]
            else:
                self.levels = [level[1]]
        for i in range(len(self.levels)):
            if isinstance(self.levels[i], Level):
                self.levels[i] = self.levels[i].name


class AtMostKInARow(_KConstraint):

    def test(self, sequence: List):
        name = self.factor.name
        for level in self.levels:
            at_most = 0
            for trial in sequence:
                if trial[name] == level:
                    at_most += 1
                    if at_most > self.trials:
                        return False
                else:
                    at_most = 0
        return True


class AtLeastKInARow(_KConstraint):

    def test(self, sequence: List):
        name = self.factor.name
        for level in self.levels:
            at_least = 0
            for trial in sequence:
                if trial[name] == level:
                    at_least += 1
                else:
                    if at_least < self.trials and at_least != 0:
                        return False
                    at_least = 0
        return True


class ExactlyKInARow(_KConstraint):

    def test(self, sequence: List):
        is_exact = True
        name = self.factor.name
        for level in self.levels:
            indexes = []
            for i in range(len(sequence)):
                trial = sequence[i]
                if trial[name] == level and (i < 0 or sequence[i - 1][name] != level):
                    indexes.append(i)
                if trial[name] == level and (i >= len(sequence) - 1 or sequence[i + 1][name] != level):
                    indexes.append(i)
            for i in range(1, len(indexes), 2):
                is_exact = is_exact and indexes[i] - indexes[i - 1] == self.trials - 1
        return is_exact


class ExactlyK(_KConstraint):

    def test(self, sequence: List):
        name = self.factor.name
        for level in self.levels:
            nr = 0
            for trial in sequence:
                if trial[name] == level:
                    nr += 1
            if nr != self.trials:
                return False
        return True


class Block:
    design: List[Factor]
    crossing: List[Factor]
    constraints: List[Constraint]
    _counter_balanced_levels: List[Level]
    _counter_balanced_names_weights: List

    def __init__(self, design: List[Factor] = None, crossing: List[Factor] = None,
                 constraints: List[Constraint] = None):
        self.design = design
        self.crossing = crossing
        self.constraints = constraints
        if not self.design:
            self.design = []
        if not self.crossing:
            self.crossing = []
        if not self.constraints:
            self.constraints = []
        # get exclude constraints:
        exclude_constraints = {}
        for factor in self.design:
            exclude_constraints[factor.name] = []
        for c in self.constraints:
            if isinstance(c, Exclude):
                exclude_constraints[c.factor] += [c.level]

        if self.crossing:
            levels = [[lvl] if lvl.name not in exclude_constraints[self.crossing[0].name] else [] for lvl in
                      self.crossing[0].levels]
            i = 1
            while i < len(self.crossing):
                list_2 = self.crossing[i].levels
                tmp = [x + [y] if y.name not in exclude_constraints[self.crossing[i].name] else [] for x in levels
                       for y in list_2]
                levels = tmp
                i += 1
            self._counter_balanced_levels = levels
            # self._counter_balanced_levels = list(filter(lambda x: x['name'] != [], self._counter_balanced_levels))
            self._counter_balanced_names_weights = []
            for level in levels:
                name = [lvl.name for lvl in level]
                weight = 1
                for lvl in level:
                    weight *= lvl.weight
                res = {'name': name, 'weight': weight}
                self._counter_balanced_names_weights.append(res)
        self._counter_balanced_levels = list(filter(lambda x: x != [], self._counter_balanced_levels))
        self._counter_balanced_names_weights = list(
            filter(lambda x: x['name'] != [], self._counter_balanced_names_weights))

    def test(self, sequence: List):
        chi_2 = self._test_crossing(sequence)
        derived_test = self._test_levels(sequence)
        constraint_test = []
        for c in self.constraints:
            constraint_test.append(c.test(sequence))
        return {'pValue': chi_2.pvalue, 'levels': derived_test, 'constraints': constraint_test}

    def _test_crossing(self, sequence: List):
        if not self.crossing:
            return chisquare([1, 1], [1, 1])
        weights_empirical = [0 for _ in self._counter_balanced_names_weights]
        for t in sequence:
            level = []
            for factor in self.crossing:
                level.append(t[factor.name])
            i = 0
            for lvl in self._counter_balanced_names_weights:
                if level == lvl['name']:
                    weights_empirical[i] += 1
                else:
                    i += 1
        weights_expected = [lvl['weight'] for lvl in self._counter_balanced_names_weights]

        # normalize weights
        # adjusting for the first trials if there is a transition window in crossing
        max_width = 0
        for factor in self.crossing:
            for lvl in factor.levels:
                if isinstance(lvl, DerivedLevel):
                    if lvl.window.width > 1:
                        max_width = max(lvl.window.width - 1, max_width)

        total_expected = sum(weights_expected) + max_width
        weights_expected = [w / total_expected * len(sequence) for w in weights_expected]

        sum_empirical = sum(weights_empirical)
        sum_expected = sum(weights_expected)
        weights_expected = [sum_empirical * w / sum_expected for w in weights_expected]
        return chisquare(weights_empirical, weights_expected)

    def _test_levels(self, sequence: List):
        test = {}
        for factor in self.design:
            test[factor.name] = True
            is_derived = False
            for lvl in factor.levels:
                if isinstance(lvl, DerivedLevel):
                    is_derived = True
            if is_derived:
                for i in range(len(sequence)):
                    trial = sequence[i]
                    for lvl in factor.levels:
                        if isinstance(lvl, DerivedLevel):
                            window = lvl.window
                            if window.width == 1:
                                args = [trial[factor_w.name] for factor_w in window.factors]
                                lvl_t = trial[factor.name]
                                if window.predicate(*args):
                                    test[factor.name] = (lvl_t == lvl.name) and test[factor.name]
                            elif i >= (window.width - 1):
                                s = i - (window.width - 1)
                                e = i + 1
                                sequence_ = sequence[s:e]
                                # indexing (0 is current trial, -1 is previous ...)
                                sequence_ = sequence_[-1] + sequence_[:-1]
                                args = [[trial[factor_w.name] for trial in sequence_] for factor_w in window.factors]
                                lvl_t = sequence_[-1][factor.name]
                                if window.predicate(*args):
                                    test[factor.name] = (lvl_t == lvl.name) and test[factor.name]

        return test
