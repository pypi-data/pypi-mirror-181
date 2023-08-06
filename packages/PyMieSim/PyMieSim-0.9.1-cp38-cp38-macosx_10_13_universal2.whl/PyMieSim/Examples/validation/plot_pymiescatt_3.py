"""
=========================
PyMieSim vs PyMieScatt: 3
=========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import validation_data_path
from PyMieSim.Experiment import SourceSet, CoreShellSet, Setup
from PyMieSim import Measure


def run():
    theoretical = numpy.genfromtxt(f"{validation_data_path}/PyMieScattQscaCoreShellMedium.csv", delimiter=',')

    diameter = numpy.geomspace(10e-9, 500e-9, 400)
    scatSet = CoreShellSet(core_diameter=diameter, shell_diameter=600e-9, core_index=1.4, shell_index=1.5, n_medium=1.2)
    source_set = SourceSet(wavelength=600e-9, polarization=None, amplitude=1)
    experiment = Setup(scatterer_set=scatSet, source_set=source_set, detector_set=None)
    data = experiment.Get(Measure.Qsca)._data.squeeze()

    plt.figure(figsize=(8, 4))
    plt.plot(diameter, data, 'C1-', linewidth=3, label='PyMieSim')

    plt.plot(diameter, theoretical, 'k--', linewidth=1, label='PyMieScatt')

    plt.xlabel(r'diameter [$\mu$m]')
    plt.ylabel('Scattering efficiency [CoreShell + n_medium]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(numpy.isclose(data, theoretical, 1e-9)), 'Error: mismatch on PyMieScatt calculation occuring'


if __name__ == '__main__':
    run()
# -
