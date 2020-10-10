import pytest
import copy
from formulabot.mep import Population, Solution


def test_Solution_init_params():

    # make sure list object passed
    with pytest.raises(ValueError):
        Solution(None, 10, 10)

    # make sure list is not empty
    with pytest.raises(ValueError):
        Solution([], 10, 10)
    
    # make sure at least 3 operations exist
    with pytest.raises(ValueError):
        Solution(['X'], 2, 10)

    # make sure at least 4 operands exist
    with pytest.raises(ValueError):
        Solution(['X'], 3, 0)

def test_Solution_init():

    parms = ['X','Y']
    operations = 5
    operands = 4

    s = Solution(parms, operations, operands)

    # the num of operations should be same as operations + params
    assert len(s.ops) == (operations + len(parms))

    # first operations are the parameters
    for i, p in enumerate(parms):
        assert p == s.ops[i][0]   
        assert s.ops[i][1] == [] 
    
    for i, o in enumerate(s.ops[len(parms):]):
        # ensure the length of the operands is correct
        assert len(o[1]) == operands

        # ensure that the operation rows referenced in the operands list
        # is less than the current operations row number
        assert len([x for x in o[1] if 0 <= x < i+len(parms)]) == operands

        # make sure the Operator is 0 < x < len(Operator)
        assert o[0] <= len(Solution.Operator)

def test_Solution_compute_contracts():

    s = Solution(['X','Y','Z'], 10, 10)

    # make sure list object passed
    with pytest.raises(ValueError):
        s.compute(None)

    with pytest.raises(ValueError):
        s.compute({})

    with pytest.raises(ValueError):
        s.compute({'X'})

def test_Solution_compute_basic_math():

    s = Solution(['X','Y','Z'], 5, 4)

    # test addition
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (1, [0, 1, 1, 1]),
            (1, [1, 2, 0, 1]),
            (1, [2, 3, 0, 4]),
            (1, [0, 1, 3, 1]),
            (1, [2, 6, 0, 5])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 11

    # test subtraction
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (2, [0, 1, 1, 1]),
            (2, [1, 2, 0, 1]),
            (2, [2, 3, 0, 4]),
            (2, [2, 1, 3, 1]),
            (2, [6, 0, 0, 5])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 3

    # test multiplication
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (3, [0, 1, 1, 1]),
            (3, [1, 2, 0, 1]),
            (3, [2, 3, 0, 4]),
            (3, [2, 1, 3, 1]),
            (3, [6, 0, 0, 5])]

    x = {'X':2, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 42

    # test division
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (4, [0, 1, 1, 1]),
            (4, [1, 2, 0, 1]),
            (4, [2, 3, 0, 4]),
            (4, [2, 1, 3, 1]),
            (4, [2, 1, 0, 5])]

    x = {'X':2, 'Y':3, 'Z':6}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 2

    # test division by zero returns zero
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (4, [0, 1, 1, 1]),
            (4, [1, 2, 0, 1]),
            (4, [2, 3, 0, 4]),
            (4, [2, 1, 3, 1]),
            (4, [2, 0, 0, 5])]

    x = {'X':0, 'Y':3, 'Z':6}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 0

    # test squareroot
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (5, [0, 1, 1, 1]),
            (5, [1, 2, 0, 1]),
            (5, [2, 3, 0, 4]),
            (5, [2, 1, 3, 1]),
            (5, [2, 0, 0, 5])]

    x = {'X':0, 'Y':3, 'Z':64}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 8

    # test squareroot, negative value
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (5, [0, 1, 1, 1]),
            (5, [1, 2, 0, 1]),
            (5, [2, 3, 0, 4]),
            (5, [2, 1, 3, 1]),
            (5, [1, 0, 0, 5])]

    x = {'X':0, 'Y':-81, 'Z':64}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 9

    # test negative value
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (6, [0, 1, 1, 1]),
            (6, [1, 2, 0, 1]),
            (6, [2, 3, 0, 4]),
            (6, [2, 1, 3, 1]),
            (6, [1, 0, 0, 5])]

    x = {'X':0, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == -3

def test_Solution_compute_trig():

    s = Solution(['X','Y','Z'], 5, 4)

    # test addition
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (7, [0, 1, 1, 1]),
            (7, [1, 2, 0, 1]),
            (7, [2, 3, 0, 4]),
            (7, [0, 1, 3, 1]),
            (7, [0, 6, 0, 5])]

    x = {'X':0, 'Y':1, 'Z':90}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 0

    # test addition
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (7, [0, 1, 1, 1]),
            (7, [1, 2, 0, 1]),
            (7, [2, 3, 0, 4]),
            (7, [0, 1, 3, 1]),
            (7, [1, 1, 0, 5])]

    x = {'X':0, 'Y':1, 'Z':90}  # test values that cant be combines unintentionally and have correct outcome
    assert round(s.compute(x), 4) == 0.8415

    # test cosine
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (8, [0, 1, 1, 1]),
            (8, [1, 2, 0, 1]),
            (8, [2, 3, 0, 4]),
            (8, [0, 1, 3, 1]),
            (8, [0, 6, 0, 5])]

    x = {'X':0, 'Y':1, 'Z':90}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 1

    # test cosine
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (8, [0, 1, 1, 1]),
            (8, [1, 2, 0, 1]),
            (8, [2, 3, 0, 4]),
            (8, [0, 1, 3, 1]),
            (8, [1, 6, 0, 5])]

    x = {'X':0, 'Y':1, 'Z':90}  # test values that cant be combines unintentionally and have correct outcome
    assert round(s.compute(x),4) == 0.5403

    # test tangent
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (9, [0, 1, 1, 1]),
            (9, [1, 2, 0, 1]),
            (9, [2, 3, 0, 4]),
            (9, [0, 1, 3, 1]),
            (9, [1, 6, 0, 5])]

    x = {'X':0, 'Y':1, 'Z':90}  # test values that cant be combines unintentionally and have correct outcome
    assert round(s.compute(x),4) == 1.5574

def test_Solution_compute_conditionals():

    s = Solution(['X','Y','Z'], 5, 4)

    # test if greater than
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (10, [0, 1, 1, 1,]),
            (10, [1, 2, 0, 1]),
            (10, [2, 3, 0, 4]),
            (10, [0, 1, 3, 1]),
            (10, [2, 1, 2, 1])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 7

    # test if greater than
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (10, [0, 1, 1, 1,]),
            (10, [1, 2, 0, 1]),
            (10, [2, 3, 0, 4]),
            (10, [0, 1, 3, 1]),
            (10, [0, 1, 2, 0])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 1

    # test if less than
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (11, [0, 1, 1, 1,]),
            (11, [1, 2, 0, 1]),
            (11, [2, 3, 0, 4]),
            (11, [0, 1, 3, 1]),
            (11, [0, 1, 2, 0])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 7

    # test if less than
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (11, [0, 1, 1, 1,]),
            (11, [1, 2, 0, 1]),
            (11, [2, 3, 0, 4]),
            (11, [0, 1, 3, 1]),
            (11, [2, 1, 2, 0])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 1

    # test if equal
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (11, [0, 1, 1, 1,]),
            (11, [1, 2, 0, 1]),
            (11, [2, 3, 0, 4]),
            (11, [0, 1, 3, 1]),
            (11, [2, 2, 1, 0])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 1

    # test if equal
    s.ops = [('X', []),
            ('Y', []),
            ('Z', []),
            (11, [0, 1, 1, 1,]),
            (11, [1, 2, 0, 1]),
            (11, [2, 3, 0, 4]),
            (11, [0, 1, 3, 1]),
            (11, [2, 1, 2, 0])]

    x = {'X':1, 'Y':3, 'Z':7}  # test values that cant be combines unintentionally and have correct outcome
    assert s.compute(x) == 1

def test_Solution_mutate():

    s1 = Solution(['X','Y','Z'], 100, 100)
    s2 = copy.deepcopy(s1)
    s2.mutate()
    assert s1.compare_operations(s2) == False

def test_Solution_compare_func():

    # check that the ops compare is the same
    s1 = Solution(['X','Y','Z'], 10, 10)
    assert s1.compare_operations(s1) == True

    # check ops compare not matched
    s2 = Solution(['X','Y','Z'], 10, 10)
    assert s1.compare_operations(s2) == False
