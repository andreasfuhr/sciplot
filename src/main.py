import contextlib
import locale
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import yaml


# neat-sciplots exception class
class NeatSciplotsException(Exception):
    pass


def get_parameters_lst(
        font_style: str,
        use_latex: bool
) -> List[object]:
    # Empty list of parameters
    parameters_lst = []

    # Path to parameter file directory
    parameters_dir = Path(__file__).parent / 'parameters'

    # Import basic parameters
    try:
        parameters_path = parameters_dir / 'basic.yml'
        with parameters_path.open() as setup_file:
            parameters = yaml.safe_load(setup_file.read())

        parameters_lst.append(parameters)
    except FileNotFoundError:
        raise NeatSciplotsException('Could not import basic parameters')

    # Import color parameters
    try:
        parameters_path = parameters_dir / 'colors.yml'
        with parameters_path.open() as setup_file:
            parameters = yaml.safe_load(setup_file.read())

        parameters_lst.append(parameters)
    except FileNotFoundError:
        raise NeatSciplotsException('Could not import typesetting parameters')

    # Import typesetting parameters
    try:
        parameters_path = parameters_dir / 'typesetting.yml'
        with parameters_path.open() as setup_file:
            parameters = yaml.safe_load(setup_file.read())

        parameters_lst.append(parameters)
    except FileNotFoundError:
        raise NeatSciplotsException('Could not import typesetting parameters')

    # Import font parameters
    try:
        parameters_path = parameters_dir / ('fonts_' + font_style + '.yml')
        with parameters_path.open() as setup_file:
            parameters = yaml.safe_load(setup_file.read())

        parameters_lst.append(parameters)
    except FileNotFoundError:
        raise NeatSciplotsException("No such font style: '" + font_style + "'")

    # Import LaTeX parameters
    if use_latex:
        try:
            parameters_path = parameters_dir / ('latex_' + font_style + '.yml')
            with parameters_path.open() as setup_file:
                parameters = yaml.safe_load(setup_file.read())

            parameters_lst.append(parameters)
        except FileNotFoundError:
            raise NeatSciplotsException("No such font style: '" + font_style + "'")

    return parameters_lst


@contextlib.contextmanager
def sciplot_style(
        use_latex: bool = True,
        theme: str = 'light',
        font_style: str = 'sans_serif',
        locale_setting: str = 'sv_SE.ISO8859-1'
):
    # Reset Matplotlib style library
    plt.style.reload_library()

    # Set locale (to get correct decimal separater etc)
    locale.setlocale(locale.LC_NUMERIC, locale_setting)

    if type == 'dark':
        plt.style.use('dark-background')
    else:
        pass

    parameters_lst = get_parameters_lst(
        font_style=font_style,
        use_latex=True
    )
    for parameters in parameters_lst:
        plt.rcParams.update(parameters)

    yield


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
        elif 'left' in loc:
            horizontal_anchor = 0.94
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
        include_black: bool = False
) -> List[str]:
    if color_no > 4 and not include_black:
        color_lst = sns.color_palette(seaborn_color_map, color_no).as_hex()
    elif color_no == 1:
        color_lst = ['000000']
    else:
        color_lst = ['000000'] + sns.color_palette(seaborn_color_map, color_no).as_hex()[:-1]

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
