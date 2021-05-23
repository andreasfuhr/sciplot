import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent / '..' / '..'))
from sciplot.main import *


def test_get_parameters_dir():
    parameters_dir = str(Path(__file__).parent / '..' / '..' / 'sciplot' / 'parameters')
    print(parameters_dir)
    assert get_parameters_dir() == str(parameters_dir)


def test_get_default_theme_lst():
    default_theme_lst = ['basic', 'typesetting', 'colors_light', 'fonts_cm_sans_serif']
    assert get_default_theme_lst() == default_theme_lst


def test_get_theme_lst_with_string():
    theme = 'theme'
    assert get_theme_lst(theme) == [theme]


def test_get_theme_lst_with_list():
    theme = ['theme1', 'theme2']
    assert get_theme_lst(theme) == theme


def test_get_theme_lst_with_float():
    theme = 100.
    with pytest.raises(SciplotException):
        theme_lst = get_theme_lst(theme)


def test_get_theme_lst_with_float_in_list():
    theme = ['theme1', 100.]
    with pytest.raises(SciplotException):
        theme_lst = get_theme_lst(theme)


def test_color_lst_one_color():
    color_no = 1
    color_lst = ['#000000']
    assert get_color_lst(color_no) == color_lst


def test_color_lst_zero_colors():
    color_no = 0
    with pytest.raises(SciplotException):
        color_lst = get_color_lst(color_no)


def test_color_lst_float_color_no():
    color_no = 2.5
    with pytest.raises(SciplotException):
        color_lst = get_color_lst(color_no)