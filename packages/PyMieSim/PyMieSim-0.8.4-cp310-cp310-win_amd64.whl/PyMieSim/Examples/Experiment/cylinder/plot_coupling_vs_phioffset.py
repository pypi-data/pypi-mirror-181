"""
==========
Goniometer
==========

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup, PhotodiodeSet
    from PyMieSim.Materials import BK7
    from PyMieSim import Measure

    detecSet = PhotodiodeSet(NA=[0.5, 0.3, 0.1, 0.05],
                             PhiOffset=np.linspace(-180, 180, 400),
                             GammaOffset=0,
                             Sampling=400,
                             Filter=None)

    scatSet = SphereSet(Diameter=2000e-9,
                        Material=BK7,
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=1200e-9,
                          Polarization=90,
                          Amplitude=1e3)

    Experiment = Setup(scatSet, sourceSet, detecSet)

    Data = Experiment.Get(Measure.Coupling)

    Data.Plot(y=Measure.Coupling, x=detecSet.PhiOffset, yScale='log', Normalize=True).Show()


if __name__ == '__main__':
    run()
