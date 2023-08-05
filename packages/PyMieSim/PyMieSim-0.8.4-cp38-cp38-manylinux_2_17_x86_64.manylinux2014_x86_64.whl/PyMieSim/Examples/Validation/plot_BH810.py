"""
============================
Bohren-Huffman (figure~8.10)
============================

"""

import numpy
import matplotlib.pyplot as plt

from PyMieSim.Tools.Directories import ValidationDataPath
from PyMieSim.Source import PlaneWave
from PyMieSim.Scatterer import Cylinder


def run():
    theoretical = numpy.genfromtxt(f"{ValidationDataPath}/Figure810BH.csv", delimiter=',')
    x = theoretical[:, 0]
    y = theoretical[:, 1]

    Source = PlaneWave(Wavelength=470e-9, Polarization=90, Amplitude=1)
    Scat = Cylinder(Diameter=3000e-9, Source=Source, Index=1.0 + 0.07j, nMedium=1.0)
    S1S2 = Scat.S1S2(Phi=x)
    Data = (numpy.abs(S1S2.S1)**2 + numpy.abs(S1S2.S2)**2) * (0.5 / (numpy.pi * Source.k))**(1 / 4)

    error = numpy.abs((Data - y) / y)

    plt.figure(figsize=(8, 4))
    plt.plot(S1S2.Phi, Data, 'C1-', linewidth=3, label='PyMieSim')

    plt.plot(x, y, 'k--', linewidth=1, label='B&H [8.10]')

    plt.xlabel('Scattering angle [degree]')
    plt.ylabel('Phase function')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    assert numpy.all(error < 1), 'Error: mismatch on BH_8.10 calculation occuring'


if __name__ == '__main__':
    run()