from collections import namedtuple
from functools import partial
import numpy as np
from scipy import stats

CI = namedtuple('ConfidenceInterval', ['point', 'low', 'high'])


def resample(data, random_state=None):
    return(data.sample(
        replace=True,
        n=len(data.index),
        random_state=random_state
    ))


def bootstrap(data, function, iterations=200):
    '''Calculates 95% CI for `function(data)`

    data:       A pandas DataFrame()
    function:   A function that takes a pd.DataFrame() and returns a numeric
    iterations: Number of iterations to run. Defaults to 1000.
    '''
    point_estimate = function(data)
    distribution = [function(resample(data, x)) for x in range(iterations)]

    return(CI(
        point_estimate,
        2*point_estimate - np.percentile(distribution, 97.5),
        2*point_estimate - np.percentile(distribution, 2.5)
    ))


def ztest(data, function):
    '''Calculates 95% CI for `function(data)`

    data:       A pandas DataFrame()
    function:   A function that takes a pd.DataFrame() and returns a numeric
    '''
    point_estimate = function(data)
    standard_error = data.sem()[0]

    return(CI(
        point_estimate,
        point_estimate - 1.96 * standard_error,
        point_estimate + 1.96 * standard_error,
    ))


def ttest(data, function):
    '''Calculates 95% CI for `function(data)`

    data:       A pandas DataFrame()
    function:   A function that takes a pd.DataFrame() and returns a numeric
    '''
    point_estimate = function(data)
    standard_error = data.sem()[0]
    observations = len(data.index)
    
    t = stats.t.ppf(0.975, df=observations-1)

    return(CI(
        point_estimate,
        point_estimate - t * standard_error,
        point_estimate + t * standard_error,
    ))


def ci_contains(ci, point):
    '''Test whether a CI contains the given point'''
    return(
        (ci.low <= point) and (point <= ci.high)
    )


def eval_ci_method(ci_method, stat_fn, population, sample_size, meta_iter=100):
    '''Test the effectiveness of a CI generation method

    To test the effectiveness of a CI generation method (e.g. bootstrapping)
    for the given population, we take `meta_iter` samples from `population`
    with `sample_size` observations. We then calculate the bootstrap CI for
    `function(sample)` for each sample and report whether the CI's include the
    true value of `function(population)`

    ci_method:   A function that takes a pd.DataFrame() and a stat_fn and
                 returns a ConfidenceInterval
    stat_fn:     A function that takes a pd.DataFrame() and returns a numeric
    population:  A DataFrame()
    sample_size: An int
    meta_iter:   An int
    '''

    true_value = stat_fn(population)
    cis = [
        ci_method(
            population.sample(n=sample_size, replace=True, random_state=x),
            stat_fn
        )
        for x in range(meta_iter)
    ]

    return([ci_contains(this_ci, true_value) for this_ci in cis])


# A convenience function for evaluating the bootstrap with eval_ci_method
eval_bootstrap = partial(eval_ci_method, ci_method=bootstrap)
