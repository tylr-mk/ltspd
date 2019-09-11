from itertools import tee

import pytest

from ltspd.schedules.decorators import randomise


@randomise
def simple_func(i):
    return i


@pytest.mark.parametrize("x", range(5, 15))
def test_randomise(x):
    i = range(x)

    o = ()
    num = 1
    for _ in range(10):
        r = simple_func(i)
        membership, order = tee(r, 2)
        assert set(membership) == set(i)
        o += (1 if tuple(order) == tuple(i) else 0,)
        num += 1
        del r

    assert sum(o) < num // 8
