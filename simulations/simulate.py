from collections import namedtuple
import numpy as np

CI = namedtuple('ConfidenceInterval', ['point', 'low', 'high'])

def resample(data):
    return(data.sample(replace=True, n=len(data.index)))


def bootstrap(data, function, iterations=100):
    '''Calculates 95% CI for `function(data)`
    
    data:       A pandas DataFrame()
    function:   A function that takes a pandas DataFrame() and returns a numeric
    iterations: Number of iterations to run. Defaults to 1000.
    '''
    point_estimate = function(data)
    distribution = [function(resample(data)) for x in range(iterations)]

    # print(point_estimate)
    # print(np.percentile(distribution, 97.5))
    # print(np.percentile(distribution, 2.5))
    # print(distribution)

    return(CI(
        point_estimate,
        2*point_estimate - np.percentile(distribution, 97.5),
        2*point_estimate - np.percentile(distribution, 2.5)
    ))


def ci_contains(ci, point):
    '''Test whether a CI contains the given point'''
    return(
        (ci.low <= point) and (point <= ci.high)
    )


def eval_bootstrap(function, population, sample_size, meta_iter=100):
    '''Test the effectiveness of Bootstrapping 

    To test the effectiveness of bootstrapping for the given population,
    we take `meta_iter` samples from `population` with `sample_size` observations.
    We then calculate the bootstrap CI for `function(sample)` for each sample
    and report whether the CI's include the true value of `function(population)`

    function:    A function that takes a pandas DataFrame() and returns a numeric
    population:  A DataFrame()
    sample_size: An int
    meta_iter:   An int
    '''

    true_value = function(population)
    cis = [
        bootstrap(population.sample(n=sample_size, replace=True), function)
        for x in range(meta_iter)
    ]

    return([ci_contains(this_ci, true_value) for this_ci in cis])
