"""
=============
Qsca vs index
=============

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import CylinderSet, SourceSet, Setup
    from PyMieSim import Measure

    scatSet = CylinderSet(diameter=800e-9,
                          index=np.linspace(1.3, 1.9, 1500),
                          n_medium=1)

    sourceSet = SourceSet(wavelength=[500e-9, 1000e-9, 1500e-9],
                          polarization=30,
                          amplitude=1)

    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet)

    Data = experiment.Get([Measure.Qsca])

    Data.Plot(y=Measure.Qsca, x=scatSet.index).Show()


if __name__ == '__main__':
    run()
