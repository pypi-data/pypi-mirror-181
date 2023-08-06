"""
==================
Qsca vs wavelength
==================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import CylinderSet, SourceSet, Setup
    from PyMieSim import Measure

    scatSet = CylinderSet(diameter=[200e-9, 150e-9, 100e-9],
                          index=[2, 3, 4],
                          n_medium=1)

    sourceSet = SourceSet(wavelength=np.linspace(400e-9, 1000e-9, 500),
                          polarization=0,
                          amplitude=1)

    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet)

    Data = experiment.Get(Input=[Measure.Qsca])

    Data.Mean(scatSet.index).Plot(y=Measure.Qsca, x=sourceSet.wavelength).Show()


if __name__ == '__main__':
    run()
