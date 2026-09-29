import random

import pytest


@pytest.fixture(autouse=True)
def _seed_random():
    """Seed the stdlib RNG so shuffle-based tests are reproducible. Several
    tests assert on shuffled output and would otherwise fail by chance, e.g. a
    3-item shuffle returns the original order 1 time in 6.
    """
    random.seed(20190912)
