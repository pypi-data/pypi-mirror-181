"""
==========
goniometer
==========

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import CylinderSet, SourceSet, Setup, PhotodiodeSet
    from PyMieSim.Materials import BK7
    from PyMieSim import Measure

    detecSet = PhotodiodeSet(NA=[0.5, 0.3, 0.1, 0.05],
                             phi_offset=np.linspace(-180, 180, 400),
                             gamma_offset=0,
                             sampling=400,
                             filter=None)

    scatSet = CylinderSet(diameter=2000e-9,
                          material=BK7,
                          n_medium=1)

    sourceSet = SourceSet(wavelength=1200e-9,
                          polarization=90,
                          amplitude=1e3)

    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet, detector_set=detecSet)

    Data = experiment.Get(Measure.coupling)

    Data.Plot(y=Measure.coupling, x=detecSet.phi_offset, y_scale='log', normalize=True).Show()


if __name__ == '__main__':
    run()
