"""
======================
coupling vs wavelength
======================
"""


def run():
    import numpy as np
    from PyMieSim.Experiment import CylinderSet, SourceSet, Setup, LPModeSet
    from PyMieSim import Measure
    from PyMieSim.Materials import BK7

    wavelength = np.linspace(950e-9, 1050e-9, 300)
    diameter = np.linspace(100e-9, 8000e-9, 5)

    detecSet = LPModeSet(Mode="1-1",
                         NA=[0.05, 0.01],
                         phi_offset=-180,
                         gamma_offset=0,
                         filter=None,
                         sampling=300)

    scatSet = CylinderSet(diameter=diameter,
                          material=BK7,
                          n_medium=1)

    sourceSet = SourceSet(wavelength=wavelength,
                          polarization=0,
                          amplitude=1)

    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet, detector_set=detecSet)

    Data = experiment.Get(Measure.coupling)

    Data.Plot(y=Measure.coupling, x=sourceSet.wavelength, std=scatSet.diameter).Show()


if __name__ == '__main__':
    run()
