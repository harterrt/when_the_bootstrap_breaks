import pandas as pd
import scipy.stats as stats
import main

def summarize_for_population(pop, name):
    df = main.eval_ci_over_sample_size(pop)
    df.to_csv('small_n/results/{0}.csv'.format(name))
    main.plot_ci_eval(df).save('small_n/results/{0}.png'.format(name))


# Look at coin flip
summarize_for_population(pd.DataFrame([0, 1]), 'coin_flip')

# Look at binomial with p=0.01
summarize_for_population(pd.DataFrame([0]*99 + [1]), 'binomial_1_pct')

# Look at pareto dist with a=3 (finite variance)
summarize_for_population(
    pd.DataFrame(stats.pareto.rvs(3, size=1000000)),
    'pereto_3'
)

# Look at pareto dist with a=1 (infinite variance)
summarize_for_population(
    pd.DataFrame(stats.pareto.rvs(1, size=1000000)),
    'pereto_1'
)
