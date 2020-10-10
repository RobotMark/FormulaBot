import pytest
from formulabot.mep import Population, Solution

__author__ = "Mark Maupin"
__copyright__ = "Mark Maupin"
__license__ = "mit"


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
        assert(len(o[1]) == operands)

        # ensure that the operation rows referenced in the operands list
        # is less than the current operations row number
        assert len([x for x in o[1] if 0 <= x < i+len(parms)]) == operands

        # make sure the Operator is 0 < x < len(Operator)
        assert o[0] < len(Solution.Operator)