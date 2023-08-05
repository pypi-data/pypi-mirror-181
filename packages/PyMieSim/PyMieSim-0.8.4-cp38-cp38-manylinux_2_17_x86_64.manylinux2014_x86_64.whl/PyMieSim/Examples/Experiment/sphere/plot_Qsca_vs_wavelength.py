"""
=======================
Qsca vs Wavelength Mean
=======================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup
    from PyMieSim import Measure

    scatSet = SphereSet(Diameter=[200e-9, 150e-9, 100e-9],
                        Index=[2, 3, 4],
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=np.linspace(400e-9, 1000e-9, 500),
                          Polarization=0,
                          Amplitude=1)

    Experiment = Setup(ScattererSet=scatSet, SourceSet=sourceSet)

    Data = Experiment.Get(Input=[Measure.Qsca])

    Data.Mean(scatSet.Index).Plot(y=Measure.Qsca, x=sourceSet.Wavelength).Show()


if __name__ == '__main__':
    run()
