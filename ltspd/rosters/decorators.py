from functools import wraps
from inspect import signature
from itertools import tee

from numpy.random import shuffle

from ltspd.utils import shuffle_second_axis
from ltspd.utils.errors import NoSolutionFoundError
from ltspd.utils.groups import explode_subgroups


def retry_roster(max_runs=10, use_exclusions=True):  # deteriorate=False, deteriorate_at=5
    """Retry for max_runs number of runs, and raise error if not successful.
    Provides a pattern for pulling, using, and amending the participants,
    exclusions, and defined groups at the time the function is called.

    As we use random shuffling of participants to essentially seed the basis
    of the roster, there is no guarantee this will work nor do we define if or
    how roster creation will not work.

    TODO: One way around that is to assume that exclusion lists are given in
    some order of priority. In which case, we provide exclusion deteriotion.
    This means the exclusions of least priority are removed after each failef
    iteration.

    :param max_runs: number of times to try (not retry) before giving up
    :type max_runs: int
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

            # shuffle particants at invocation
            if this_run.get("randomise"):
                shuffle(this_run["participants"])
            else:
                return f(**this_run)

            # provide an exit if any return is acceptable
            if not use_exclusions:
                return f(**this_run)

            # provide the set up for evaluating failure and retry
            # identify all excluded groups for this run
            this_run["exclusions"] |= set(explode_subgroups(
                this_run["exclusions"], this_run.get("group_size")
            ))

            runs = 0
            # deteriotation allows us to remove exclusion groups from the tail
            # which if ordered means we can remove the weaker limits.
            # attrition_rate = round(len(this_run["exclusions"]) / max_runs)
            while runs < max_runs:
                roster, check = tee(iter(f(**this_run)), 2)
                if not set(check) & this_run["exclusions"]:
                    return roster
                # if deteriorate and runs > deteriorate_at:
                #     this_run["exclusions"] = (
                #         this_run["exclusions"][:-attrition_rate]
                #     )
                runs += 1
            # Case if no return on last run, raise obscured in block to prevent
            # always being raised
            if True:
                raise NoSolutionFoundError(
                    "No solution found while running {}() {} times. Process "
                    "Aborted. You may rerun, but be aware there may be no "
                    "solution.".format(f.__name__, max_runs)
                )

        return f_retry  # true decorator

    return retryable


def retry_group_roster(
    max_runs=10, use_exclusions=True, deteriorate=False, deteriorate_at=5
):
    """Retry for max_runs number of runs, and raise error if not successful.
    Provides a pattern for pulling, using, and amending the participants,
    exclusions, and defined groups at the time the function is called.

    As we use random shuffling of participants to essentially seed the basis
    of the roster, there is no guarantee this will work nor do we define if or
    how roster creation will not work.

    TODO: One way around that is to assume that exclusion lists are given in
    some order of priority. In which case, we provide exclusion deteriotion.
    This means the exclusions of least priority are removed after each failed
    iteration.

    :param max_runs: number of times to try (not retry) before giving up
    :type max_runs: int
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

            # shuffle groups at invocation or return if order given
            if this_run.get("randomise"):
                shuffle_second_axis(this_run["groups"])
            else:
                return f(**this_run)

            # provide an exit if any return is acceptable
            if not use_exclusions:
                return f(**this_run)

            # provide the set up for evaluating failure and retry
            # identify all excluded groups for this run
            this_run["exclusions"] |= set(explode_subgroups(
                this_run["exclusions"], this_run["group_size"]
            ))

            runs = 0
            # deteriotation allows us to remove exclusion groups from the tail
            # which if ordered means we can remove the weaker limits.
            # attrition_rate = round(len(this_run["exclusions"]) / max_runs)
            while runs < max_runs:
                try:
                    roster, check = tee(iter(f(**this_run)), 2)
                    if not set(check) & this_run["exclusions"]:
                        return roster
                except NoSolutionFoundError:
                    runs += 1
                # if deteriorate and runs > deteriorate_at:
                #     this_run["exclusions"] = (
                #         this_run["exclusions"][:-attrition_rate]
                #     )

            try:
                output = f(**this_run)
                if output:
                    return output
            except NoSolutionFoundError:
                raise NoSolutionFoundError(
                    "No solution found while running {}() {} times. Process "
                    "Aborted. You may rerun, but be aware there may be no "
                    "solution.".format(f.__name__, max_runs)
                )

        return f_retry  # true decorator

    return retryable
