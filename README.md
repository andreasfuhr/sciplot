# neat-sciplots
*Neatly format Matplotlib scientific plots*

**neat-sciplots** is a Python package that *neatly* formats scientific plots created with Matplotlib in a 
user-friendly, yet highly customizable way.
It makes typesetting in LaTeX possible and comes with several methods that makes plotting more 
straightforward and less cluttered, without sacrificing full control over plot settings.
An example of a plot created with neat-sciplots is shown below.

<img src="example_plots/Line_plot_2021-05-15T19.03.png" alt="example_plot" width="400"/>

[example image](./example_plots/Line_plot_2021-05-15T19.03.png){ width=50% }

The neat-sciplots package was developed by [Andreas Führ](https://www.linkedin.com/in/fuhrandreas/) in May 2021.

## Installation and getting started
To install the latest release from PyPi, execute the following command:
```
pip install neat-sciplots
```
To install the latest commit, please use the the following command:
```
pip install git+https://github.com/andreasfuhr/neat-sciplots.git
```

<br/><br/>
Formatting plots in Matplotlib is based on a functional `with`-statement context. A MWE can be demonstrated as follows:
```python
import matplotlib.pyplot as plt
import sciplot

# Define x and y...

with sciplot.style():
    plt.plot(x, y)
    plt.show()
```
If a LaTeX distribution is not available, `use_latex=False` must be passed as an argument to `sciplot.style()`.


## Overview

### Key Features:
* Implements LaTeX kernel for typesetting Matplotlib plots. A versatile preamble is included that is specifically 
created and optionally editable for mathematics- and physics-oriented papers, theses and presentations.
* Easy customization. The user is encouraged edit the accessible and highly readable YAML parameters files, whom can 
be found with the `sciplot.get_paramters_dir()`-method
* Includes a set of useful methods relevant during plotting:
    * `sciplot.set_size_cm()` for setting figure sizes in centimeters
    * `sciplot.set_legend()` for customizing the content and position of plot legends
    * `sciplot.get_color_lst()` for extracting a list of colors of specified length and from a given Seaborn colormap
    * `sciplot.save_time_stamped_figure` for saving plots in an easy manner with time stamped file names


### Disadvantages:
* Slow. LaTeX figures can take quite some time to compile. Loading the parameters is however not known to be time 
consuming.
* Only compatible with Python 3.7 and later. The 3.3.4 version of Matplotlib fixes several bugs that directly solves 
some earlier issues with this package. 






It should be noted that although this package is in many ways similar to [[1]](#1), which is a highly recommended 
alternative, neat-sciplots has been independently developed and has a multitude of structural and functional differences.


## Using neat-sciplots

TBD


## Citing neat-plots

To cite this Python package, please use the following BibTeX citation:

```
@article{neat-sciplots,
  author       = {Andreas H. Führ},
  title        = {{andreasfuhr/neat-sciplots}},
  month        = may,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {0.0.1},
  doi          = {10.5281/zenodo.4764827},
  url          = {http://doi.org/10.5281/zenodo.4764827}
}
```
Note that under the current license, citing this package is not necessary. The creator will however be happy and 
thankful for any recognition.


## Future improvements

The package is still in its infancy and is planned to be expanded in features and configurability. Here is a list of 
what is in the pipeline:
* Documentation of source code
* Instructions on how to install a local LaTeX distribution
* Making it possible to choose LaTeX fonts. As of currently, *Computer Modern Roman* and *Computer Modern Roman Sans 
Serif* are the only two font options for both text and mathematical notation.
* Test suite for further code development
* Include example plots in documentation
* Write instructions on how to use the package


## References
<a id="1">[1]</a>
J.D. Garrett and H. Peng,
*garrettj403/SciencePlots*,
ver. 1.0.7.
Zenodo,
Feb. 2021.
\[Online].
DOI: [10.5281/zenodo.4106649](http://doi.org/10.5281/zenodo.4106649)