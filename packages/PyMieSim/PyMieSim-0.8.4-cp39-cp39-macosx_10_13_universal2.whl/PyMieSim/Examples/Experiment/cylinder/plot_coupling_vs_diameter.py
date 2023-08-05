"""
====================
Coupling vs Diameter
====================

"""


def run():
    import numpy
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup, PhotodiodeSet
    from PyMieSim import Measure
    from PyMieSim.Materials import BK7

    scatSet = SphereSet(Diameter=numpy.linspace(100e-9, 3000e-9, 200),
                        Material=BK7,
                        nMedium=1.0)

    sourceSet = SourceSet(Wavelength=1200e-9,
                          Polarization=90,
                          Amplitude=1)

    detecSet = PhotodiodeSet(NA=[0.1, 0.05],
                             PhiOffset=-180.0,
                             GammaOffset=0.0,
                             Sampling=600,
                             Filter=None)

    Experiment = Setup(scatSet, sourceSet, detecSet)

    Data = Experiment.Get([Measure.Coupling])

    Data.Plot(y=Measure.Coupling, x=scatSet.Diameter, yScale='linear', Normalize=True).Show()


if __name__ == '__main__':
    run()
