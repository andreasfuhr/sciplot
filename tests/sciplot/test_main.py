import locale
import sys
from pathlib import Path
import pytest
import numpy as np
from scipy.stats import pareto
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path
import locale

sys.path.append(str(Path(__file__).parent / '..' / '..'))
import sciplot.main as sciplot

locale.setlocale(locale.LC_NUMERIC, 'en_US')

def test_get_parameters_dir():
    parameters_dir = str(Path(__file__).parent / '..' / '..' / 'sciplot' / 'parameters')
    print(parameters_dir)
    assert sciplot.get_parameters_dir() == str(parameters_dir)


def test_get_theme_priority_lst():
    theme_priority_lst = [
        'alpha',
        'beta',
        'gamma',
        'no-latex',
        'serif',
        'sans-serif',
        'dark',
        'default'
    ]
    assert sciplot.get_theme_priority_lst() == theme_priority_lst


def test_get_theme_lst_with_string():
    theme = 'theme'
    assert sciplot._get_theme_lst(theme) == [theme]


def test_get_theme_lst_with_capital_string():
    theme = 'THEME'
    assert sciplot._get_theme_lst(theme) == [theme.lower()]


def test_get_theme_lst_with_list():
    theme = ['theme1', 'theme2']
    assert sciplot._get_theme_lst(theme) == theme


def test_get_theme_lst_with_float():
    theme = 100.
    with pytest.raises(sciplot.SciplotException):
        theme_lst = sciplot._get_theme_lst(theme)


def test_get_theme_lst_with_float_in_list():
    theme = ['theme1', 100.]
    with pytest.raises(sciplot.SciplotException):
        theme_lst = sciplot._get_theme_lst(theme)


def test_color_lst_one_color():
    color_no = 1
    color_lst = ['#000000']
    assert sciplot.get_color_lst(color_no) == color_lst


def test_color_lst_zero_colors():
    color_no = 0
    with pytest.raises(sciplot.SciplotException):
        color_lst = sciplot.get_color_lst(color_no)


def test_color_lst_float_color_no():
    color_no = 2.5
    with pytest.raises(sciplot.SciplotException):
        color_lst = sciplot.get_color_lst(color_no)


def test_style_locale_en_US():
    locale = 'en_US'
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(locale_setting=locale):
        plt.plot(x, y)
        return plt.fig


def test_style_locale_incorrect():
    local = 'Undefined_local'
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with pytest.raises(locale.Error):
        with sciplot.style(locale_setting=local):
            plt.plot(x, y)
            return plt.fig


def test_get_available_locals():
    sciplot.get_available_locals()


def test_style_empty():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme='no-latex', locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_default():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme='no-latex', locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_clean():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'clean'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_dark():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'dark'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'serif'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_clean_sans_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['clean', 'sans-serif'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_no_latex():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme='no-latex', locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_no_latex_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'serif'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_basic():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'basic'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_typesetting():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'typesetting'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_colors_light():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'colors_light'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_colors_dark():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'colors_dark'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_fonts_cm_sans_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'fonts_cm_sans_serif'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_fonts_cm_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'fonts_cm_serif'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_latex_sans_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'latex_sans_serif'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_latex_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(theme=['no-latex', 'latex_serif'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


def test_style_alpha_beta_gamma():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(['no-latex', 'alpha', 'beta', 'gamma'], locale_setting='en_US.UTF-8'):
        plt.plot(x, y)
        return plt.fig


# Plot 1
@pytest.mark.mpl_image_compare
def test_plot_1():
    with sciplot.style(theme='no-latex', locale_setting='en_US.UTF-8'):
        x_m = 2  # scale
        alpha_lst = [1, 2, 3, 4]  # shape parameters
        x = np.linspace(0, 6, 1000)

        pdf = np.array([pareto.pdf(x, scale=x_m, b=a) for a in alpha_lst])

        sciplot.set_size_cm(7)
        fig, ax = plt.subplots(1, 1)

        fig.suptitle(r'Pareto PDF' +
                     r' $p(x \,|\, x_\mathrm{m}, \alpha) = \frac{\alpha x_\mathrm{m}^\alpha}{x^{\alpha+1}}$' +
                     r' with $x_\mathrm{m}=2$')

        line_plot = ax.plot(x, pdf.T)

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

        return fig


# Plot 2
@pytest.mark.mpl_image_compare
def test_plot_2():
    with sciplot.style(theme=['no-latex', 'dark'], locale_setting='en_US.UTF-8'):
        np.random.seed(42)
        n = 10000
        mean_ar = np.array([4.5, 6.1, 8.3])
        std_ar = np.array([0.2, 0.9, 0.5])
        data_ar = np.array([
            np.random.normal(mean_ar[0], std_ar[0], n),
            np.random.normal(mean_ar[1], std_ar[1], n),
            np.random.normal(mean_ar[2], std_ar[2], n)
        ])

        sciplot.set_size_cm(16, 8)
        fig, ax = plt.subplots(1, 1)

        fig.suptitle('Histogram of normally distributed velocities with ' + str(n) + ' samples')


        plot_lst = []
        color_lst = sciplot.get_color_lst(len(data_ar), seaborn_color_map='rocket', colorful=False)

        for i, data in enumerate(data_ar):
            ax.hist(data, density=True, bins=100, alpha=0.7, color=color_lst[i])
            plot_lst.append(Rectangle((0, 0), 1, 1, color=color_lst[i], alpha=0.7))

        label_lst = []
        for i in range(len(data_ar)):
            label_lst.append(r'$\mu=' + str(mean_ar[i]) + '$, $\sigma=' + str(std_ar[i]) + '$')

        sciplot.set_legend(
            ax=ax,
            plot_tpl=tuple(plot_lst),
            label_tpl=tuple(label_lst),
            loc='lower right',
            outside_plot=True
        )

        ax.set_xlabel('Velocity (m/s)')
        ax.set_ylabel(r'Relative frequency')

        return fig