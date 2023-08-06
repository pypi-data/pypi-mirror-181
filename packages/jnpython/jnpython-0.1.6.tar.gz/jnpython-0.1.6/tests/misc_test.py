import pytest
from jnpython.misc import euclidean_distance


def test_euclidean_distance():
    v1 = (1,2,3)
    v2 = (1,2,3)
    assert euclidean_distance(v1,v2) == 0
    v1 = (0,0)
    v2 = (3,4)
    assert euclidean_distance(v1,v2) == 5
