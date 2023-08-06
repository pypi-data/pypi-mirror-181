"""
===================
b1 vs core diameter
===================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SourceSet, Setup, CoreShellSet
    from PyMieSim.Materials import BK7
    from PyMieSim import Measure

    scatSet = CoreShellSet(core_diameter=np.geomspace(100e-09, 3000e-9, 5000),
                           shell_diameter=800e-9,
                           core_index=1.6,
                           shell_material=BK7,
                           n_medium=1)

    sourceSet = SourceSet(wavelength=[800e-9],
                          polarization=0,
                          amplitude=1)

    experiment = Setup(scatterer_set=scatSet, source_set=sourceSet)

    data = experiment.Get([Measure.a1])

    data.Plot(y=Measure.a1, x=scatSet.core_diameter, y_scale='linear').Show()


if __name__ == '__main__':
    run()
