import simulate as sim
import pandas as pd
import numpy as np


def mean(x):
    return(np.mean(x)[0])


def summarize_meta_bootstrap(population):
    return(sim.bootstrap(
        pd.DataFrame(sim.eval_bootstrap(mean, population, 100)),
        mean
    ))


print(
    "Cheeky confidence intervals for "
    "how often our confidence intervals are right:"
)


print('\nBinomial p=0.5')
print(summarize_meta_bootstrap(pd.DataFrame([0, 1])))


print('\nBinomial p=0.01')
print(summarize_meta_bootstrap(pd.DataFrame([0]*99 + [1])))


print('\nBinomial p=0.99')
print(summarize_meta_bootstrap(pd.DataFrame([0] + [1]*99)))
