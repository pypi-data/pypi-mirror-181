from sweetpea import *
import time


def weighted():
    test_factor = Factor('test_1', [Level('a', 3), Level('b', 11)])
    test_factor_2 = Factor('test_2', [Level('c', 7), Level('d', 5)])

    design = [test_factor, test_factor_2]
    crossing = [test_factor, test_factor_2]

    block = CrossBlock(design, crossing, [])
    experiment = synthesize_trials(block, 1)
    return experiment


def weighted_manually():
    l_a = [f'a{i}' for i in range(3)]
    l_b = [f'b{i}' for i in range(11)]
    l_c = [f'c{i}' for i in range(7)]
    l_d = [f'd{i}' for i in range(5)]
    test_factor = Factor('test_1', l_a + l_b)
    test_factor_2 = Factor('test_2', l_c + l_d)

    design = [test_factor, test_factor_2]
    crossing = [test_factor, test_factor_2]

    block = CrossBlock(design, crossing, [])
    experiment = synthesize_trials(block, 1)
    return experiment


if __name__ == '__main__':
    start = time.time()
    weighted_manually()
    print(f'manually: {time.time()-start}')
    start = time.time()
    weighted()
    print(f'weighted: {time.time() - start}')
