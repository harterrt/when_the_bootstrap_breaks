import simulate as sim
import pandas as pd
import numpy as np

coin_flip = pd.DataFrame({'x':[0, 1]})
mean = lambda x: np.mean(x)[0]

bootstrap_results = sim.eval_bootstrap(mean, coin_flip, 100)

# Success rate
print(np.mean(bootstrap_results))

print(
    "Cheeky confidence intervals for "
    "how often our confidence intervals are right:"
)
print(sim.bootstrap(pd.DataFrame(bootstrap_results), mean))
