"""
====================
coupling vs diameter
====================

"""


def run():
    import numpy
    from PyMieSim.Experiment import CoreShellSet, SourceSet, Setup, PhotodiodeSet
    from PyMieSim import Measure
    from PyMieSim.Materials import BK7, Silver

    scatSet = CoreShellSet(core_diameter=numpy.geomspace(100e-09, 600e-9, 400),
                           shell_diameter=800e-9,
                           core_material=Silver,
                           # shell_index=1.4,
                           shell_material=BK7,
                           n_medium=1)

    sourceSet = SourceSet(wavelength=1200e-9,
                          polarization=90,
                          amplitude=1)

    detecSet = PhotodiodeSet(NA=[0.1, 0.05],
                             phi_offset=-180.0,
                             gamma_offset=0.0,
                             sampling=600,
                             filter=None)

    experiment = Setup(scatSet, sourceSet, detecSet)

    data = experiment.Get([Measure.coupling])

    data.Plot(y=Measure.coupling, x=scatSet.core_diameter, y_scale='linear', normalize=True).Show()


if __name__ == '__main__':
    run()
