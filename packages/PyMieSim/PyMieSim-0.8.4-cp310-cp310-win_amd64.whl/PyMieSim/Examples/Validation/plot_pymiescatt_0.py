"""
=========================
PyMieSim vs PyMieScatt: 0
=========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import ValidationDataPath
from PyMieSim.Experiment import SourceSet, SphereSet, Setup
from PyMieSim import Measure


def run():
    theoretical = numpy.genfromtxt(f"{ValidationDataPath}/PyMieScattQscaMedium.csv", delimiter=',')

    Diameter = numpy.geomspace(10e-9, 6e-6, 800)
    scatSet = SphereSet(Diameter=Diameter, Index=1.4, nMedium=1.21)
    sourceSet = SourceSet(Wavelength=632.8e-9, Polarization=[None], Amplitude=1)
    ExpSet = Setup(ScattererSet=scatSet, SourceSet=sourceSet, DetectorSet=None)
    Data = ExpSet.Get(Measure.Qsca).Data.squeeze()

    plt.figure(figsize=(8, 4))
    plt.plot(Diameter, Data, 'C1-', linewidth=3, label='PyMieSim')

    plt.plot(Diameter, theoretical, 'k--', linewidth=1, label='PyMieScatt')

    plt.xlabel(r'Diameter [$\mu$m]')
    plt.ylabel('Scattering efficiency [Sphere + nMedium]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(numpy.isclose(Data, theoretical, 1e-9)), 'Error: mismatch on PyMieScatt calculation occuring'


if __name__ == '__main__':
    run()