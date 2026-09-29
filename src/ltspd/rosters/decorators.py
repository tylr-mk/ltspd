from functools import wraps
from inspect import signature
from random import shuffle

from ltspd.utils import shuffle_second_axis
from ltspd.utils.errors import NoSolutionFoundError


def violates_exclusions(roster, exclusions):
    """True if any group in the roster contains every member of an exclusion.

    An exclusion of ("Terrence", "Phillip") is violated by the group
    ("Phillip", "Karen", "Terrence") as much as by ("Terrence", "Phillip"), so
    membership is compared as sets rather than as ordered tuples.

    :param roster: iterable of groups
    :param exclusions: iterable of groups of members that must not share a group
    """
    exclusion_sets = [set(e) for e in exclusions]
    return any(e <= set(group) for group in roster for e in exclusion_sets)


def _retry(shuffle_input, max_runs, use_exclusions):
    """Build a retrying decorator around a roster generator.

    The decorated function is re-run, re-shuffling its input each time via
    shuffle_input(arguments), until it yields a roster that violates none of the
    exclusions or max_runs attempts have been made.

    As we use random shuffling of participants to essentially seed the basis
    of the roster, there is no guarantee this will work nor do we define if or
    how roster creation will not work.

    TODO: One way around that is to assume that exclusion lists are given in
    some order of priority. In which case, we provide exclusion deterioration.
    This means the exclusions of least priority are removed after each failed
    iteration.
    """

    def retryable(f):
        # caching the signature at this point means that the signature is
        # only required once at defining the decorated function which helps
        # with performance as inspect is quite costly.
        sig_cache = signature(f)

        @wraps(f)
        def f_retry(*args, **kwargs):
            # create the bind arguments which gives access to all the arg
            # values at invocation
            arguments = sig_cache.bind(*args, **kwargs)
            arguments.apply_defaults()
            this_run = arguments.arguments

            # return as given if order is fixed or any return is acceptable
            if not this_run.get("randomise"):
                return f(**this_run)
            if not use_exclusions:
                shuffle_input(this_run)
                return f(**this_run)

            exclusions = list(this_run.get("exclusions") or ())
            for _ in range(max_runs):
                shuffle_input(this_run)
                try:
                    roster = tuple(f(**this_run))
                except NoSolutionFoundError:
                    continue
                if not violates_exclusions(roster, exclusions):
                    return iter(roster)

            raise NoSolutionFoundError(
                f"No solution found while running {f.__name__}() {max_runs} times. "
                "Process Aborted. You may rerun, but be aware there may be no "
                "solution."
            )

        return f_retry  # true decorator

    return retryable


def _shuffle_participants(arguments):
    shuffle(arguments["participants"])


def _shuffle_groups(arguments):
    arguments["groups"] = [list(g) for g in arguments["groups"]]
    shuffle_second_axis(arguments["groups"])


def retry_roster(max_runs=10, use_exclusions=True):
    """Retry for max_runs number of runs, and raise error if not successful.
    Shuffles the decorated function's participants on every run.

    :param max_runs: number of times to try (not retry) before giving up
    :type max_runs: int
    """
    return _retry(_shuffle_participants, max_runs, use_exclusions)


def retry_group_roster(max_runs=10, use_exclusions=True):
    """Retry for max_runs number of runs, and raise error if not successful.
    Shuffles the members within each of the decorated function's groups on
    every run.

    :param max_runs: number of times to try (not retry) before giving up
    :type max_runs: int
    """
    return _retry(_shuffle_groups, max_runs, use_exclusions)
