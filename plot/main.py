import pandas as pd
from plotnine import ggplot, aes, scale_x_log10, ylim, geom_hline, geom_line

names = [
    'coin_flip', 'binomial_1_pct', 'pereto_1', 'pereto_3'
]

def make_plot(name):
    df = pd.read_csv(f'small_n/results/{name}.csv')

    molten = pd.melt(
        df,
        id_vars = ['sample_size'],
        value_vars = ['bootstrap', 'ztest', 'ttest'],
        var_name = 'method',
        value_name = 'success',
    )

    (
        ggplot(molten, aes(x='sample_size', y='success', color='method'))
        + geom_line(size=1)
        + scale_x_log10()
        + ylim(0, 1)
        + geom_hline(yintercept=0.95, linetype='dotted', color='#FF5500', size=3)
    ).save(
        f'slides/static/plots/{name}.png',
        height=7.0,
        width=10,
        units='in'
    )

for name in names:
    make_plot(name)
