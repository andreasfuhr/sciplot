import contextlib
import csv
import locale
import logging
import os
import re
import warnings
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Union, OrderedDict

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

# Reset Matplotlib style library (use in case of unresolved errors)
# plt.style.reload_library()

# Disable "findfont: Font family ['serif'] not found. Falling back to DejaVu Sans."
logging.getLogger('matplotlib.font_manager').disabled = True

# Dark mode boolean operator
dark_mode = False


# sciplot warning class
class SciplotWarning(UserWarning):
    pass


# sciplot exception class
class SciplotException(Exception):
    pass


def _get_theme_lst(theme_input):
    theme_lst = []
    if isinstance(theme_input, str):
        theme_lst.append(theme_input)
    elif isinstance(theme_input, list):
        for theme in theme_input:
            if not isinstance(theme, str):
                raise SciplotException(
                    "Incorrect theme input type in list for theme '" +
                    str(theme) +
                    "': '" +
                    str(type(theme_input)) +
                    "'. Correct input type is 'str'.")
        theme_lst = theme_input
    else:
        raise SciplotException(
            "Incorrect theme input type: '" +
            str(type(theme_input)) +
            "'. Correct input type is 'str' or 'list'.")

    # Remove double entries and make theme inputs lowercase
    theme_lst = [theme.lower() for theme in OrderedDict.fromkeys(theme_lst)]

    return theme_lst


def _get_default_theme_lst(
        theme_lst: List[str]
) -> List[str]:
    if 'clean' in theme_lst:
        if 'default' in theme_lst:
            theme_lst.remove('default')

        theme_lst.remove('clean')
    else:
        if not 'default' in theme_lst:
            theme_lst.append('default')

    return theme_lst


def _get_parameter_file_lst(
        theme: str
) -> List[str]:
    if theme == 'default':
        parameter_file_lst = ['basic', 'typesetting', 'colors_light', 'fonts_cm_sans_serif', 'latex_sans_serif']
    elif theme == 'dark':
        plt.style.use('dark_background')
        global dark_mode
        dark_mode = True
        parameter_file_lst = ['colors_dark']
    elif theme == 'serif':
        parameter_file_lst = ['fonts_cm_serif', 'latex_serif']
    elif theme == 'sans-serif':
        parameter_file_lst = ['fonts_cm_sans_serif', 'latex_sans_serif']
    elif theme == 'no-latex':
        parameter_file_lst = ['no_latex']
    else:
        parameter_file_lst = [theme]

    return parameter_file_lst


def _theme_exists(
        theme: str
) -> bool:
    if not (theme in get_theme_priority_lst()):
        try:
            parameters_dir = Path(__file__).parent / 'parameters'
            parameters_path = parameters_dir / (theme + '.yml')
            with parameters_path.open():
                pass
            return True
        except FileNotFoundError:
            warnings.warn("Invalid theme ignored by Sciplot: '" + theme + "'", SciplotWarning)
            return False
    else:
        return False


def _get_parameters_lst(
        parameter_file_lst: List[str]
) -> List[object]:
    # Empty list of parameters
    parameters_lst = []

    parameters_dir = Path(__file__).parent / 'parameters'

    # Import parameters
    for parameter_file in parameter_file_lst:
        try:
            parameters_path = parameters_dir / (parameter_file + '.yml')
            with parameters_path.open() as setup_file:
                parameters = yaml.safe_load(setup_file.read())
                if parameters:
                    parameters_lst.append(parameters)
        except FileNotFoundError:
            raise SciplotException(
                "Unable to import theme parameter file: '" + parameter_file + "'")

    return parameters_lst


@contextlib.contextmanager
def style(
        theme: Union[str, List[str]] = 'default',
        locale_setting: str = 'sv_SE.ISO8859-1'
):
    # Set locale (to get correct decimal separater etc)
    locale.setlocale(locale.LC_NUMERIC, locale_setting)

    # Get requested themes as list
    theme_lst = _get_theme_lst(theme)

    # Get list with or without default theme
    theme_lst = _get_default_theme_lst(theme_lst)

    # Get ordered list if parameter files
    parameter_file_lst = []
    theme_priority_lst = get_theme_priority_lst()
    theme_priority_lst.reverse()

    # Add themes' associated parameter files to list
    for theme_priority in theme_priority_lst:
        for theme in theme_lst:
            if theme == theme_priority:
                parameter_file_lst += _get_parameter_file_lst(theme)

    # Add user defined themes to parameter_file_lst
    if any(theme not in theme_priority_lst for theme in theme_lst):
        for theme in theme_lst:
            if _theme_exists(theme):
                parameter_file_lst += _get_parameter_file_lst(theme)

    # Get list of parameter objects from file list
    parameters_lst = _get_parameters_lst(parameter_file_lst)

    # Set all parameters in list
    for parameters in parameters_lst:
        plt.rcParams.update(parameters)

    yield

    plt.style.use('default')
    global dark_mode
    dark_mode = False


def get_parameters_dir() -> str:
    return str(Path(__file__).parent / 'parameters')


def get_theme_priority_lst() -> List[str]:
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
    return theme_priority_lst


def get_available_locals():
    locales_file_path = Path(__file__).parent / 'parameters' / 'locales.csv'
    with open(locales_file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter='\t')
        print('=' * 89 + '\n', ' ' * 35, 'Available locales', ' ' * 35, '\n' + '=' * 89 + '\n')
        print('{0:<30}{1:<20}{2}'.format(*['Locale', 'Code set', 'Description']))
        print('-' * 89)
        for row in csv_reader:
            print('{0:<30}{1:<20}{2}'.format(*row))


def set_size_cm(
        width: float,
        height: float = None
):
    if height is None:
        height = width

    cm2in = 1 / 2.54
    plt.rcParams['figure.figsize'] = (width * cm2in, height * cm2in)


def set_legend(
        ax: matplotlib.axes.Axes,
        plot_tpl: Tuple[matplotlib.artist.Artist],
        label_tpl: Tuple[str],
        loc: str = 'lower left',
        outside_plot: bool = False,
        handle_scale_factor: float = 5.
):
    if outside_plot:
        if 'right' in loc:
            horizontal_anchor = 1.04
            loc = loc.replace('right', 'left')
        elif 'left' in loc:
            horizontal_anchor = 0.94
            loc = loc.replace('left', 'right')
        else:
            horizontal_anchor = 0.5

        if 'upper' in loc:
            vertical_anchor = 1.
        elif 'lower' in loc:
            vertical_anchor = 0.
        else:
            vertical_anchor = 0.5

        lgnd = ax.legend(
            plot_tpl,
            label_tpl,
            scatterpoints=1,
            loc=loc,
            bbox_to_anchor=(horizontal_anchor, vertical_anchor)
        )
    else:
        lgnd = ax.legend(
            plot_tpl,
            label_tpl,
            scatterpoints=1,
            loc=loc,
        )

    for lgnd_handle in lgnd.legendHandles:
        lgnd_handle._sizes = [handle_scale_factor]


def get_color_lst(
        color_no: int,
        seaborn_color_map: str = 'cubehelix',
        colorful: bool = False
) -> List[str]:
    if color_no == 0 or not isinstance(color_no, int):
        raise SciplotException("Invalid number of colors: '" + str(color_no) + "'")

    if color_no > 4 and colorful:
        color_lst = sns.color_palette(seaborn_color_map, color_no).as_hex()
    elif color_no == 1 and not dark_mode:
        color_lst = ['#000000']
    elif color_no == 1 and dark_mode:
        color_lst = ['#FFFFFF']
    elif not colorful and dark_mode:
        color_lst = sns.color_palette(seaborn_color_map, color_no).as_hex()[:-1] + ['#FFFFFF']
    else:
        color_lst = ['#000000'] + sns.color_palette(seaborn_color_map, color_no).as_hex()[:-1]

    return color_lst


def save_time_stamped_figure(
        plot_file_name: str,  # filnamn/filsökväg med eller utan ändelse, t.ex. .png eller .pdf
        save_directory: str = '',  # valfri uppdelning i filnamn och mappsökväg
        file_type: str = 'png'  # filtyp
):
    time_stamp = datetime.today().strftime('%Y-%m-%dT%H.%M')
    if 'png' in plot_file_name:
        plot_file_name = str(re.sub(r'\.png$', '', plot_file_name))
    elif 'pdf' in plot_file_name:
        plot_file_name = str(re.sub(r'\.pdf$', '', plot_file_name))

    if save_directory == '':
        plot_file_path = plot_file_name + '_' + time_stamp + '.' + file_type
    else:
        plot_file_path = os.path.join(
            save_directory,
            plot_file_name + '_' + time_stamp + '.' + file_type
        )

    plt.savefig(plot_file_path, bbox_inches='tight', pad_inches=0.04)
