import simulate as sim
import pandas as pd
import numpy as np


def mean(x):
    return(np.mean(x)[0])


coin_flip = pd.DataFrame({'x': [0, 1]})
bootstrap_results = sim.eval_bootstrap(mean, coin_flip, 100)

print(
    "Cheeky confidence intervals for "
    "how often our confidence intervals are right:"
)
print(sim.bootstrap(pd.DataFrame(bootstrap_results), mean))
