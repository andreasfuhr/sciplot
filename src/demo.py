import numpy as np
from scipy.stats import pareto
import matplotlib.pyplot as plt

import src.main as sciplot

with sciplot.sciplot_style():

    xm = 1  # scale
    alpha_lst = [1, 2, 3]  # shape parameters
    x = np.linspace(0, 5, 1000)

    output = np.array([pareto.pdf(x, scale=xm, b=a) for a in alpha_lst])

    sciplot.set_size_cm(7)
    fig, ax = plt.subplots(1, 1)

    fig.suptitle(r'Pareto PDF $p(x \,|\, x_\mathrm{m}, \alpha) = \frac{\alpha x_\mathrm{m}^\alpha}{x^{\alpha+1}}$' +
                 r' with $x_\mathrm{m}=1$')

    line_plot = ax.plot(x, output.T)

    label_lst = []
    for alpha in alpha_lst:
        label_lst.append(r'$\alpha=' + str(alpha) + '$')

    sciplot.set_legend(
        ax=ax,
        plot_tpl=line_plot,
        label_tpl=tuple(label_lst),
        loc='upper right'
    )

    ax.set_xlabel('$x$')
    ax.set_ylabel(r'$p(x \,|\, x_\mathrm{m}, \alpha)$')
    plt.show()