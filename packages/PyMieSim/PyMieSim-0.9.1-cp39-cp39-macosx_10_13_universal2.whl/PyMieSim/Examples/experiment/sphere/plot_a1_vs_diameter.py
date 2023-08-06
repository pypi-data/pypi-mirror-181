"""
=========================
a1 scattering coefficient
=========================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup
    from PyMieSim import Measure

    scatSet = SphereSet(diameter=np.linspace(100e-9, 10000e-9, 1000),
                        index=1.4,
                        n_medium=1)

    sourceSet = SourceSet(wavelength=400e-9,
                          polarization=0,
                          amplitude=1)

    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet)

    Data = experiment.Get(Input=[Measure.a1])

    Data.Plot(y=Measure.a1, x=scatSet.diameter).Show()


if __name__ == '__main__':
    run()
