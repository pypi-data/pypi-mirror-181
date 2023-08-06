"""
=========================
PyMieSim vs PyMieScatt: 0
=========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import validation_data_path
from PyMieSim.Experiment import SourceSet, SphereSet, Setup
from PyMieSim import Measure


def run():
    theoretical = numpy.genfromtxt(f"{validation_data_path}/PyMieScattQscaMedium.csv", delimiter=',')

    diameter = numpy.geomspace(10e-9, 6e-6, 800)
    scatSet = SphereSet(diameter=diameter, index=1.4, n_medium=1.21)
    source_set = SourceSet(wavelength=632.8e-9, polarization=[None], amplitude=1)
    ExpSet = Setup(scatterer_set=scatSet, source_set=source_set, detector_set=None)
    data = ExpSet.Get(Measure.Qsca)._data.squeeze()

    plt.figure(figsize=(8, 4))
    plt.plot(diameter, data, 'C1-', linewidth=3, label='PyMieSim')

    plt.plot(diameter, theoretical, 'k--', linewidth=1, label='PyMieScatt')

    plt.xlabel(r'diameter [$\mu$m]')
    plt.ylabel('Scattering efficiency [Sphere + n_medium]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(numpy.isclose(data, theoretical, 1e-9)), 'Error: mismatch on PyMieScatt calculation occuring'


if __name__ == '__main__':
    run()
# -
