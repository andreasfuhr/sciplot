import matplotlib.pyplot as plt
import numpy as np
import sciplot
from pathlib import Path

x = np.arange(0, 2 * np.pi, 1e-2)
y1 = np.sin(2 * x + np.pi)
y2 = np.cos(2 * x + np.pi)

sciplot.set_size_cm(5)

with sciplot.style():
    plt.plot(x, y1, x, y2)
    plt.xticks(
        np.linspace(0, 2 * np.pi, 5),
        ['$0$', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    )

    sciplot.save_time_stamped_figure(
        plot_file_name='MWE_plot',
        save_directory=(Path(__file__).parent)
    )
    plt.show()