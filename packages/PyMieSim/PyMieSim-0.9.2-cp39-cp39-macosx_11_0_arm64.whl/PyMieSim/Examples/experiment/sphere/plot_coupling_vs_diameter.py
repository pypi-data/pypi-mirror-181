"""
====================
Coupling vs diameter
====================

"""


def run():
    import numpy
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup, PhotodiodeSet
    from PyMieSim import Measure
    from PyMieSim.Materials import BK7

    scatSet = SphereSet(diameter=numpy.linspace(100e-9, 3000e-9, 200),
                        material=BK7,
                        n_medium=1.0)

    sourceSet = SourceSet(wavelength=1200e-9,
                          polarization=90,
                          amplitude=1)

    detecSet = PhotodiodeSet(NA=[0.1, 0.05],
                             phi_offset=-180.0,
                             gamma_offset=0.0,
                             sampling=600,
                             filter=None)

    Experiment = Setup(scatSet, sourceSet, detecSet)

    Data = Experiment.Get([Measure.coupling])

    Data.Plot(y=Measure.coupling, x=scatSet.diameter, y_scale='linear', normalize=True).Show()


if __name__ == '__main__':
    run()
