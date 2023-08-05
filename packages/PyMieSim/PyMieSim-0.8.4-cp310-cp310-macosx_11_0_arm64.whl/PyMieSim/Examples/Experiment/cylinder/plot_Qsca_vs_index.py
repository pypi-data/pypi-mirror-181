"""
==================
Mean Qsca vs Index
==================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup
    from PyMieSim import Measure

    scatSet = SphereSet(Diameter=800e-9,
                        Index=np.linspace(1.3, 1.9, 1500),
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=[500e-9, 1000e-9, 1500e-9],
                          Polarization=30,
                          Amplitude=1)

    Experiment = Setup(ScattererSet=scatSet, SourceSet=sourceSet)

    Data = Experiment.Get([Measure.Qsca])

    Data.Plot(y=Measure.Qsca, x=scatSet.Index).Show()


if __name__ == '__main__':
    run()
