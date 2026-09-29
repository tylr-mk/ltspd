from functools import wraps
from random import shuffle


def randomise(f):
    """Simply shuffle the output of the function, if the function output is
    shufflable everything is fine, otherwise we convert to a list and return
    a list iterator object from the thing.
    """

    @wraps(f)
    def f_retry(*args, **kwargs):
        o = f(*args, **kwargs)
        try:
            shuffle(o)
            return o
        except TypeError:
            o = list(o)
            shuffle(o)
            return iter(o)

    return f_retry  # true decorator
