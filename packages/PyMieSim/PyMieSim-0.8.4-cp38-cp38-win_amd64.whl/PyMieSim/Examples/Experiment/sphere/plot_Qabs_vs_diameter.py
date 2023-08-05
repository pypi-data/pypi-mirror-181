"""
================
Qsca vs Diameter
================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup
    from PyMieSim.Materials import Gold, Silver, Aluminium
    from PyMieSim import Measure

    scatSet = SphereSet(Diameter=np.linspace(1e-09, 800e-9, 300),
                        Material=[Silver, Gold, Aluminium],
                        nMedium=1)

    sourceSet = SourceSet(Wavelength=400e-9,
                          Polarization=0,
                          Amplitude=1)

    Experiment = Setup(ScattererSet=scatSet,
                       SourceSet=sourceSet)

    Data = Experiment.Get(Input=[Measure.Qabs])

    Data.Plot(y=Measure.Qabs, x=scatSet.Diameter, yScale="log").Show()


if __name__ == '__main__':
    run()
