"""
=====================
Mean Qsca vs Diameter
=====================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup
    from PyMieSim.Materials import FusedSilica
    from PyMieSim import Measure

    Diameter = np.geomspace(6.36e-09, 10000e-9, 200500)
    Wavelength = [500e-9, 1000e-9, 1500e-9]

    scatSet = SphereSet(Diameter=Diameter,
                        Index=[1.4],
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=Wavelength,
                          Polarization=30,
                          Amplitude=1)

    Experiment = Setup(ScattererSet=scatSet, SourceSet=sourceSet)

    Data = Experiment.Get(Measure.Qsca)

    Data.Plot(y=Measure.Qsca, x=scatSet.Diameter).Show()


if __name__ == '__main__':
    run()
