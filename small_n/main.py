import pandas as pd
import numpy as np
from functools import partial
from plotnine import ggplot, aes, geom_line, scale_x_log10, ylim
import plotnine as pn

from simulations import simulate as sim

def mean(data):
    return(np.mean(data)[0])


def eval_ci_over_sample_size(population):
    sample_sizes = [2**x for x in range(4, 15)]  # 16 through 16384

    def eval(ci_method):
        out = []
        for x in sample_sizes:
            print('Working on sample_size = {0}'.format(x))
            out.append(np.mean(sim.eval_ci_method(
                ci_method,
                mean,
                population,
                x,
                meta_iter=1000
            )))

        return(out)

    df = pd.DataFrame({
        'sample_size': sample_sizes,
        'bootstrap': eval(sim.bootstrap),
        'ztest': eval(sim.ztest),
        'ttest': eval(sim.ttest),
    })

    return(df)


def plot_ci_eval(df):
    molten = pd.melt(
        df,
        id_vars=['sample_size'],
        value_vars=['bootstrap', 'ztest', 'ttest']
    )


    return(
        ggplot(molten, aes(x='sample_size', y='value', color='variable'))
        + geom_line()
        + scale_x_log10()
        + ylim(0, 1)
    )



