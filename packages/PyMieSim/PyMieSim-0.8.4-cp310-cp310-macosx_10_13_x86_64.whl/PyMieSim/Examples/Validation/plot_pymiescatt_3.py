"""
=========================
PyMieSim vs PyMieScatt: 3
=========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import ValidationDataPath
from PyMieSim.Experiment import SourceSet, CoreShellSet, Setup
from PyMieSim import Measure


def run():
    theoretical = numpy.genfromtxt(f"{ValidationDataPath}/PyMieScattQscaCoreShellMedium.csv", delimiter=',')

    Diameter = numpy.geomspace(10e-9, 500e-9, 400)
    scatSet = CoreShellSet(CoreDiameter=Diameter, ShellDiameter=600e-9, CoreIndex=1.4, ShellIndex=1.5, nMedium=1.2)
    sourceSet = SourceSet(Wavelength=600e-9, Polarization=None, Amplitude=1)
    ExpSet = Setup(ScattererSet=scatSet, SourceSet=sourceSet, DetectorSet=None)
    Data = ExpSet.Get(Measure.Qsca).Data.squeeze()

    plt.figure(figsize=(8, 4))
    plt.plot(Diameter, Data, 'C1-', linewidth=3, label='PyMieSim')

    plt.plot(Diameter, theoretical, 'k--', linewidth=1, label='PyMieScatt')

    plt.xlabel(r'Diameter [$\mu$m]')
    plt.ylabel('Scattering efficiency [CoreShell + nMedium]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(numpy.isclose(Data, theoretical, 1e-9)), 'Error: mismatch on PyMieScatt calculation occuring'
    

if __name__ == '__main__':
    run()