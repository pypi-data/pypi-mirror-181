"""
======================
Coupling vs Wavelength
======================
"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup, LPModeSet
    from PyMieSim import Measure
    from PyMieSim.Materials import BK7

    Wavelength = np.linspace(950e-9, 1050e-9, 300)
    Diameter = np.linspace(100e-9, 8000e-9, 5)

    detecSet = LPModeSet(Mode="1-1",
                         NA=[0.05, 0.01],
                         PhiOffset=-180,
                         GammaOffset=0,
                         Filter=None,
                         Sampling=300)

    scatSet = SphereSet(Diameter=Diameter,
                        Material=BK7,
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=Wavelength,
                          Polarization=0,
                          Amplitude=1)

    Experiment = Setup(scatSet, sourceSet, detecSet)

    Data = Experiment.Get(Measure.Coupling)

    Data.Plot(y=Measure.Coupling, x=sourceSet.Wavelength, Std=scatSet.Diameter).Show()


if __name__ == '__main__':
    run()
