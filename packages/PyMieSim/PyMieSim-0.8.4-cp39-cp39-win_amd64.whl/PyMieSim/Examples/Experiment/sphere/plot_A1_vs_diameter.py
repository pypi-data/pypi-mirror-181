"""
=========================
A1 scattering coefficient
=========================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup
    from PyMieSim import Measure

    scatSet = SphereSet(Diameter=np.linspace(100e-9, 10000e-9, 800),
                        Index=1.4,
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=400e-9,
                          Polarization=0,
                          Amplitude=1)

    Experiment = Setup(ScattererSet=scatSet, SourceSet=sourceSet)

    Data = Experiment.Get(Input=[Measure.a1])

    Data.Plot(y=Measure.a1, x=scatSet.Diameter).Show()


if __name__ == '__main__':
    run()
