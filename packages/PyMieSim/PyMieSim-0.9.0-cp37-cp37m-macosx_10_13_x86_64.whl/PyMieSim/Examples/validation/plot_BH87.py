"""
===========================
Bohren-Huffman (figure~8.7)
===========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import validation_data_path
from PyMieSim.Experiment import SourceSet, CylinderSet, Setup
from PyMieSim import Measure


def run():
    theoretical = numpy.genfromtxt(f"{validation_data_path}/Figure87BH.csv", delimiter=',')

    diameter = numpy.geomspace(10e-9, 6e-6, 800)
    volume = numpy.pi * (diameter / 2)**2
    scatSet = CylinderSet(diameter=diameter, index=1.55, n_medium=1.)
    sourceSet = SourceSet(wavelength=632.8e-9, polarization=[0, 90], amplitude=1)
    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet, detector_set=None)
    data = experiment.Get(Measure.Csca)._data.squeeze() / volume * 1e-4 / 100

    plt.figure(figsize=(8, 4))
    plt.plot(diameter, data[0], 'b--', linewidth=3, label='PyMieSim')
    plt.plot(diameter, data[1], 'r-', linewidth=3, label='PyMieSim')

    plt.plot(diameter, theoretical[0], 'k--', linewidth=1, label='BH 8.8')
    plt.plot(diameter, theoretical[1], 'k--', linewidth=1, label='BH 8.8')

    plt.xlabel(r'diameter [$\mu$m]')
    plt.ylabel('Scattering cross section [Cylinder]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(numpy.isclose(data, theoretical, 1e-9)), 'Error: mismatch on BH_8.7 calculation occuring'


if __name__ == '__main__':
    run()
# -
