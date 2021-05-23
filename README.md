# Sciplot
[<img src='https://img.shields.io/pypi/v/sciplot/0.7.9'>](https://pypi.org/project/sciplot/) 
[<img src='https://img.shields.io/static/v1?label=repo&color=blue&style=flat&logo=github&message=v.0.7.9'>](https://github.com/andreasfuhr/sciplot)

*Format Matplotlib scientific plots*

**Sciplot** is an alpha version Python package that formats scientific plots created with Matplotlib in a 
user-friendly, yet highly customizable way.
It makes typesetting in LaTeX possible and comes with several methods that makes plotting more 
straightforward and less cluttered, without sacrificing full control over plot settings.

Two examples of plots that have been created with Sciplot:

<img src='https://github.com/andreasfuhr/sciplot/raw/7a1b143b5101a5e9b19f03cf654a1060a7f3a489/example_plots/Line_plot_2021-05-23T13.37.png' alt="example_plot" width="500"/>
<img src="https://github.com/andreasfuhr/sciplot/raw/7a1b143b5101a5e9b19f03cf654a1060a7f3a489/example_plots/Histogram_plot_2021-05-23T13.38.png" alt="example_plot" width="800"/>

The Sciplot package was developed by [Andreas Führ](https://www.linkedin.com/in/fuhrandreas/) in May 2021.

## Installation and getting started
To install the latest release from PyPI, execute the following command:
```
pip install sciplot
```
To install the latest commit, please use the the following command:
```
pip install git+https://github.com/andreasfuhr/sciplot.git
```

<br/><br/>
Formatting plots in Matplotlib is based on a functional `with`-statement context. A MWE can be demonstrated as follows:
```python
import matplotlib.pyplot as plt
import numpy as np
import sciplot

x = np.arange(0, 2 * np.pi, 1e-2)
y1 = np.sin(2 * x + np.pi)
y2 = np.cos(2 * x + np.pi)

sciplot.set_size_cm(5)  # Alternatively set size with Matplotlib directly

with sciplot.style():
    plt.plot(x, y1, x, y2)
    plt.xticks(
        np.linspace(0, 2 * np.pi, 5),
        ['$0$', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    )
    plt.show()
```
This produces the following output:
<img src='https://github.com/andreasfuhr/sciplot/raw/7a1b143b5101a5e9b19f03cf654a1060a7f3a489/example_plots/MWE_plot_2021-05-23T13.33.png' alt="example_plot" width="500"/>


If a LaTeX distribution is not available, `use_latex=False` must be passed as an argument to `sciplot.style()`.
For demonstrations of plotting that covers all packages features, see either 
[`example_plots.py`](example_plots/example_plots.py) in the [`example_plots`](./example_plots) directory.

## Overview

### Key Features:
* User-friendly. A *style context manager* is used for all Matplotlib related user code and can be passed several 
arguments to alter the look of the plot, such as:
    * LaTeX typesetting
    * serif or sans serif font
    * dark mode
    * [locale](https://docs.oracle.com/cd/E23824_01/html/E26033/glset.html) string (for correct decimal 
    separator etc.)
* Implements LaTeX kernel for typesetting plots. A versatile LaTeX preamble is included that is specifically 
created and optionally editable for mathematics- and physics-oriented papers, theses and presentations. Both the 
[siunitx](https://ctan.org/pkg/siunitx) and [physics](https://www.ctan.org/pkg/physics) LaTeX packages are for example
included by default in the parameter settings.
* Easy customization. Most settings have been moved to parameters files, which are imported to the context manager and 
configured with `matplotlibrc`. The **user is encouraged to edit** these accessible and highly readable YAML parameters
files, whom can be found with the `sciplot.get_paramters_dir()` method.
* Includes a set of useful methods relevant during plotting:
    * `sciplot.set_size_cm()` for setting figure sizes in centimeters
    * `sciplot.set_legend()` for customizing the content and position of plot legends
    * `sciplot.get_color_lst()` for extracting a list of colors of specified length and from a given Seaborn colormap
    * `sciplot.save_time_stamped_figure` for saving plots in an easy manner with time stamped file names


### Disadvantages:
* Slow. LaTeX figures can take quite some time to compile. Loading the parameters is however not known from experience
to be time consuming.
* Only compatible with Python 3.7 and later. The 3.3.4 version of Matplotlib fixes several bugs that directly solves 
some earlier issues with this package. 


It should be noted that although this package is in many ways similar to [[1]](#1), which is a recommended 
alternative approach, Sciplot has been independently developed and has a multitude of structural and functional 
differences.


## Citing Sciplot

To cite this Python package, please use the following BibTeX citation:

```
@article{Sciplot,
  author       = {Andreas H. Führ},
  title        = {{andreasfuhr/sciplot}},
  month        = may,
  year         = 2021,
  version      = {0.7.9},
  url          = {https://github.com/andreasfuhr/sciplot}
}
```
Note that under the current license, citing this package is not necessary. The creator will however be happy and 
thankful for any recognition.


## Future improvements

The package is still in its infancy and is planned to be expanded in features and configurability. Here is a list of 
what is in the pipeline:
* Change name of package
* Documentation of source code
* Instructions on how to install a local LaTeX distribution
* Making it possible to choose LaTeX fonts. As of currently, *Computer Modern Roman* and *Computer Modern Roman Sans 
Serif* are the only two font options for both text and mathematical notation.
* Test suite for further code development
* Include example plots in documentation
* Write instructions on how to use the package
* Add themes. Let `sciplot.style()` take the argument `theme=str` *or* `theme=List[str]`. This will be a big 
change to how the `sciplot.main` module works.
* Add a set of *empty* themes that makes it easy for a user to add their own themes

### Table of proposed themes:

Name of theme                            | Priority | Background color | Font                         | Seaborn colormap | Figure size
:--------------------------------------- | :------- | :--------------- | :--------------------------- | :--------------- | :----------
***default***<sup id="a1">[1](#f1)</sup> | high     | white            | CMR Sans Serif               | cubehelix        | -
***dark***                               | high     | black            | -                            | -                | -
***antique***                            | low      | white            | Garamond                     | *TBD*            | -
***ieee_column***                        | medium   | white            | ?<sup id="a1">[2](#f2)</sup> | *TBD*            | 88 mm<sup id="a1">[3](#f3)</sup>
***ieee_page***                          | low      | white            | ?<sup id="a1">[2](#f2)</sup> | *TBD*            | 181 mm<sup id="a1">[3](#f3)</sup>
***grid***                               | high

<b id="f1">1</b>: Initialised at start of context.

<b id="f2">2</b>: One of the following Open Type fonts are suggested to be used: Times New Roman, Helvetica, Arial, 
Cambria or Symbol [[2]](#2).

<b id="f3">3</b>: See [[2]](#2) for a description of sizes that graphics should be.


## References
<a id="1">[1]</a>
J.D. Garrett and H. Peng,
*garrettj403/SciencePlots*,
ver. 1.0.7.
Zenodo,
Feb. 2021.
\[Online].
doi: [10.5281/zenodo.4106649](http://doi.org/10.5281/zenodo.4106649)

<a id="2">[2]</a>
"Preparation of papers for IEEE Transactions and Journals (December 2013),"
in IEEE Transactions on Consumer Electronics,
vol. 63,
no. 1,
pp. c3-c3,
February 2017,
doi: [10.1109/TCE.2017.7932035](http://doi.org/10.1109/TCE.2017.7932035)