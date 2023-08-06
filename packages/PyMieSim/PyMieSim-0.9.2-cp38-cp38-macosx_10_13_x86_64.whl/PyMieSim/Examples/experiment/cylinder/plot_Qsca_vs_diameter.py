"""
================
Qsca vs diameter
================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import CylinderSet, SourceSet, Setup
    from PyMieSim import Measure

    diameter = np.geomspace(6.36e-09, 10000e-9, 200500)
    wavelength = [500e-9, 1000e-9, 1500e-9]

    scatSet = CylinderSet(diameter=diameter,
                          index=[1.4],
                          n_medium=1)

    sourceSet = SourceSet(wavelength=wavelength,
                          polarization=30,
                          amplitude=1)

    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet)

    Data = experiment.Get(Measure.Qsca)

    Data.Plot(y=Measure.Qsca, x=scatSet.diameter).Show()


if __name__ == '__main__':
    run()
