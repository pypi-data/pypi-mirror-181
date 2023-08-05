"""
===========================
Bohren-Huffman (figure~8.8)
===========================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import ValidationDataPath
from PyMieSim.Experiment import SourceSet, CylinderSet, Setup
from PyMieSim import Measure


def run():
    theoretical = numpy.genfromtxt(f"{ValidationDataPath}/Figure88BH.csv", delimiter=',')

    Diameter = numpy.geomspace(10e-9, 6e-6, 800)
    Volume = numpy.pi * (Diameter / 2)**2
    scatSet = CylinderSet(Diameter=Diameter, Index=1.55, nMedium=1.335)
    sourceSet = SourceSet(Wavelength=632.8e-9, Polarization=[0, 90], Amplitude=1)
    ExpSet = Setup(ScattererSet=scatSet, SourceSet=sourceSet, DetectorSet=None)
    Data = ExpSet.Get(Measure.Csca).Data.squeeze() / Volume * 1e-4 / 100

    plt.figure(figsize=(8, 4))
    plt.plot(Diameter, Data[0], 'C0-', linewidth=3, label='PyMieSim')
    plt.plot(Diameter, Data[1], 'C1-', linewidth=3, label='PyMieSim')

    plt.plot(Diameter, theoretical[0], 'k--', linewidth=1, label='BH 8.8')
    plt.plot(Diameter, theoretical[1], 'k--', linewidth=1, label='BH 8.8')

    plt.xlabel(r'Diameter [$\mu$m]')
    plt.ylabel('Scattering cross section [Cylinder]')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(numpy.isclose(Data, theoretical, 1e-9)), 'Error: mismatch on BH_8.8 calculation occuring'


if __name__ == '__main__':
    run()