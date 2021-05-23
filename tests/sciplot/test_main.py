import locale
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest

sys.path.append(str(Path(__file__).parent / '..' / '..'))
import sciplot.main as sciplot


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


def test_style_locale_C():
    locale = 'C'
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(locale_setting=locale):
        plt.plot(x, y)
        plt.close()


def test_style_locale_incorrect():
    local = 'Undefined_local'
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with pytest.raises(locale.Error):
        with sciplot.style(locale_setting=local):
            plt.plot(x, y)
            plt.close()


def test_get_available_locals():
    sciplot.get_available_locals()


def test_get_matplotlibrc_reference():
    sciplot.get_matplotlibrc_reference()


def test_style_empty():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style():
        plt.plot(x, y)
        plt.close()


def test_style_default():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style():
        plt.plot(x, y)
        plt.close()


def test_style_clean():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('clean'):
        plt.plot(x, y)
        plt.close()


def test_style_dark():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('dark'):
        plt.plot(x, y)
        plt.close()


def test_style_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('serif'):
        plt.plot(x, y)
        plt.close()


def test_style_clean_sans_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(['clean', 'sans-serif']):
        plt.plot(x, y)
        plt.close()


def test_style_no_latex():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('no-latex'):
        plt.plot(x, y)
        plt.close()


def test_style_no_latex_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(['no-latex', 'serif']):
        plt.plot(x, y)
        plt.close()


def test_style_basic():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('basic'):
        plt.plot(x, y)
        plt.close()


def test_style_typesetting():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('typesetting'):
        plt.plot(x, y)
        plt.close()


def test_style_colors_light():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('colors_light'):
        plt.plot(x, y)
        plt.close()


def test_style_colors_dark():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('colors_dark'):
        plt.plot(x, y)
        plt.close()


def test_style_fonts_cm_sans_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('fonts_cm_sans_serif'):
        plt.plot(x, y)
        plt.close()


def test_style_fonts_cm_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('fonts_cm_serif'):
        plt.plot(x, y)
        plt.close()


def test_style_latex_sans_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('latex_sans_serif'):
        plt.plot(x, y)
        plt.close()


def test_style_latex_serif():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style('latex_serif'):
        plt.plot(x, y)
        plt.close()


def test_style_alpha_beta_gamma():
    x = np.linspace(0, 1, 2)
    y = 2 * x
    with sciplot.style(['alpha', 'beta', 'gamma']):
        plt.plot(x, y)
        plt.close()
