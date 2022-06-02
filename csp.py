from collections import defaultdict
from functools import reduce

import itertools
import re
import random



###############################################################################################################
############################################ UTILITY #######################################################
###############################################################################################################

identity = lambda x: x

argmin = min

def shuffled(iterable):
    """ RANDOMLY SHUFFLE A COPY OF ITERABLE """
    items = list(iterable)
    random.shuffle(items)
    return items

def first(iterable, default=None):
    """Return the first element of an iterable or the next element of a generator; or default."""
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

def argmin_random_tie(seq, key=identity):
    """Return a minimum element of seq; break ties at random."""
    return argmin(shuffled(seq), key=key)

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)





##########################################
######### Backtracking Algorithm #########
##########################################

def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result