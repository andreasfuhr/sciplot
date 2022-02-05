import contextlib
import csv
import glob
import json
import locale
import logging
import os
import re
import warnings
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

# Reset Matplotlib style library (use in case of unresolved errors)
# plt.style.reload_library()

# Disable "findfont: Font family ['serif'] not found. Falling back to DejaVu Sans."
#logging.getLogger('mpl.font_manager').disabled = True

# Dark mode boolean operator
dark_mode = False

# Parameter dictionary for Matplotlib RC
RC_PARAMS = {}

# List of Sciplot themes with parameters
THEME_PARAMS = {}

# List of themes with descending priority
PRIORITY_THEME_LST = [
        'no-latex',
        'serif',
        'sans-serif',
        'dark',
        'default'
    ]

# sciplot warning class
class SciplotWarning(UserWarning):
    pass


# sciplot exception class
class SciplotException(Exception):
    pass


def _load_theme_parameters():
    global THEME_PARAMS
    param_filepath_general = str(Path(__file__).parent / 'parameters' / '*.yaml')
    for param_filepath in glob.iglob(param_filepath_general):
        with open(param_filepath, 'r') as param_file:
            THEME_PARAMS[str(Path(param_filepath).stem)] = yaml.safe_load(param_file.read())


def _get_theme_paramters():
    return THEME_PARAMS


def _parse_themes(
    themes_input: Union[str, dict, List[str], List[dict], List[Union[str, dict]]]
    ) -> Tuple[List[str], List[dict]]:
    if isinstance(themes_input, str):
        return [themes_input], None
    elif isinstance(themes_input, dict):
        return None, [themes_input]
    elif isinstance(themes_input, list):
        theme_lst = []
        custom_param_lst = []
        for theme in themes_input:
            if isinstance(theme, str):
                theme_lst.append(theme)
            elif isinstance(theme, dict):
                custom_param_lst.append(theme)
            else:
                raise SciplotException(f"Incorrect theme input type in list for themes '{theme}': {type(theme)}. "
                                       f"Correct input types is 'str' or 'dict'.")

        if not theme_lst:
            return None, {param for param in custom_param_lst}
        elif not custom_param_lst:
            return list(set(themes_input)), None
        else:
            return list(set(themes_input)), {param for param in custom_param_lst}
    else:
        raise SciplotException(f"Incorrect theme input type: '{type(themes_input)}'. Correct input type is 'str' or "
                               f"'list'.")


def _get_default_theme_lst(
        theme_lst: List[str]
) -> List[str]:
    if 'clean' in theme_lst:
        if 'default' in theme_lst:
            theme_lst.remove('default')

        theme_lst.remove('clean')
    else:
        if 'default' not in theme_lst:
            theme_lst.append('default')

    return theme_lst


def _get_theme_parameter_lst(
        theme: str
) -> List[str]:
    if theme == 'default':
        theme_param_lst = ['basic', 'typesetting', 'colors_light', 'fonts_cm_sans_serif', 'latex_sans_serif']
    elif theme == 'dark':
        plt.style.use('dark_background')
        global dark_mode
        dark_mode = True
        theme_param_lst = ['colors_dark']
    elif theme == 'serif':
        theme_param_lst = ['fonts_cm_serif', 'latex_serif']
    elif theme == 'sans-serif':
        theme_param_lst = ['fonts_cm_sans_serif', 'latex_sans_serif']
    elif theme == 'no-latex':
        theme_param_lst = ['no_latex']

    return theme_param_lst


def _theme_exists(
        theme: str
) -> bool:
    return theme in PRIORITY_THEME_LST


def _get_parameters_dct(
        prio_theme_lst: List[str]
) -> dict:
    tot_theme_param_lst = []
    prio_theme_lst.reverse()
    for theme in prio_theme_lst:
        tot_theme_param_lst += [param for param in _get_theme_parameter_lst(theme) if param not in prio_theme_lst]
    
    # Empty list of parameters
    parameters_dct = {}
    for param in tot_theme_param_lst:
        parameters_dct.update(THEME_PARAMS[param])

    return parameters_dct


@contextlib.contextmanager
def style(
    themes: Union[str, List[str], dict] = 'default'
):
    parameters_dct = {}

    # Get requested themes as list and list of custom parameter dictionaries
    theme_lst, custom_param_lst = _parse_themes(themes)

    if theme_lst:
        # Get list with or without default theme
        theme_lst = _get_default_theme_lst(theme_lst)

        # Check that themes exist
        for theme in theme_lst:
            if not _theme_exists(theme):
                raise SciplotException(f"Theme '{theme}' does not exist. Choose from: " + ', '.join(PRIORITY_THEME_LST))

        # Get ordered list if parameter files
        prio_theme_lst = [theme for theme in PRIORITY_THEME_LST if theme in theme_lst]

        # Get final dictionary of parameters from prioritized list of themes
        parameters_dct = _get_parameters_dct(prio_theme_lst)

    if custom_param_lst:
        # Add custom theme parameters
        for custom_param in custom_param_lst:
            parameters_dct.update(custom_param)

    # Set global RC parameters variable
    global RC_PARAMS
    RC_PARAMS = parameters_dct

    # Plot with temporary Matplotlib parameters
    with mpl.rc_context(RC_PARAMS):
        yield

    # Reset global variables
    RC_PARAMS = {}
    global dark_mode
    dark_mode = False


def get_parameters_dir() -> str:
    return str(Path(__file__).parent / 'parameters')


def print_locales():
    locales_file_path = Path(__file__).parent / 'parameters' / 'locales.csv'
    with open(locales_file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter='\t')
        print('=' * 89 + '\n', ' ' * 35, 'Available locales', ' ' * 35, '\n' + '=' * 89 + '\n')
        print('{0:<30}{1:<20}{2}'.format(*['Locale', 'Code set', 'Description']))
        print('-' * 89)
        for row in csv_reader:
            print('{0:<30}{1:<20}{2}'.format(*row))

def print_parameters():
    print(json.dumps(RC_PARAMS, indent=3))


def set_locale(locale_setting):
    # Set locale (to get correct decimal separater etc)
    locale.setlocale(locale.LC_NUMERIC, locale_setting)


def set_size_cm(
        width: float,
        height: float = None
):
    if height is None:
        height = width

    cm2in = 1 / 2.54
    plt.rcParams['figure.figsize'] = (width * cm2in, height * cm2in)


def set_legend(
        ax: mpl.axes.Axes,
        plot_tpl: Tuple[mpl.artist.Artist],
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


_load_theme_parameters()