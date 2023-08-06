"""
================
Qsca vs diameter
================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import CylinderSet, SourceSet, Setup
    from PyMieSim.Materials import Gold, Silver, Aluminium
    from PyMieSim import Measure

    scatSet = CylinderSet(diameter=np.linspace(1e-09, 800e-9, 300),
                          material=[Silver, Gold, Aluminium],
                          n_medium=1)

    sourceSet = SourceSet(wavelength=400e-9,
                          polarization=0,
                          amplitude=1)

    Experiment = Setup(scatterer_set=scatSet, source_set=sourceSet)

    Data = Experiment.Get(Input=[Measure.Qabs])

    Data.Plot(y=Measure.Qabs, x=scatSet.diameter, y_scale="log").Show()


if __name__ == '__main__':
    run()
