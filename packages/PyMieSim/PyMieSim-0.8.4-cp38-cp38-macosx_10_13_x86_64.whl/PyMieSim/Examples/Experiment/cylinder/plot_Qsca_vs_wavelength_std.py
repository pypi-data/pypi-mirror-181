"""
=======================
Qsca vs Wavelength STD
=======================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup
    from PyMieSim.Materials import Silver
    from PyMieSim import Measure

    Diameter = np.linspace(400e-9, 1400e-9, 10)
    Wavelength = np.linspace(200e-9, 1800e-9, 300)

    scatSet = SphereSet(Diameter=Diameter,
                        Material=Silver,
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=Wavelength,
                          Polarization=None,
                          Amplitude=1)

    Experiment = Setup(scatSet, sourceSet)

    Data = Experiment.Get(Measure.Qsca)

    Data.Plot(y=Measure.Qsca, x=sourceSet.Wavelength, yScale='log', Std=scatSet.Diameter).Show()


if __name__ == '__main__':
    run()
