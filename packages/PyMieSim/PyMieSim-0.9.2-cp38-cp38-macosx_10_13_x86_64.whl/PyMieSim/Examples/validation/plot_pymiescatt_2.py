"""
=========================
PyMieSim vs PyMieScatt: 2
=========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import validation_data_path
from PyMieSim.Experiment import SourceSet, CoreShellSet, Setup
from PyMieSim import Measure


def run():
    theoretical = numpy.genfromtxt(f"{validation_data_path}/PyMieScattQscaCoreShell.csv", delimiter=',')

    diameter = numpy.geomspace(10e-9, 500e-9, 400)
    scatSet = CoreShellSet(core_diameter=diameter, shell_diameter=600e-9, core_index=1.4, shell_index=1.5, n_medium=1.0)
    sourceSet = SourceSet(wavelength=600e-9, polarization=None, amplitude=1)
    ExpSet = Setup(scatterer_set=scatSet, source_set=sourceSet, detector_set=None)
    data = ExpSet.Get(Measure.Qsca)._data.squeeze()

    plt.figure(figsize=(8, 4))
    plt.plot(diameter, data, 'C1-', linewidth=3, label='PyMieSim')

    plt.plot(diameter, theoretical, 'k--', linewidth=1, label='PyMieScatt')

    plt.xlabel(r'diameter [$\mu$m]')
    plt.ylabel('Scattering efficiency [CoreShell]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(numpy.isclose(data, theoretical, 1e-9)), 'Error: mismatch on PyMieScatt calculation occuring'


if __name__ == '__main__':
    run()
# -
