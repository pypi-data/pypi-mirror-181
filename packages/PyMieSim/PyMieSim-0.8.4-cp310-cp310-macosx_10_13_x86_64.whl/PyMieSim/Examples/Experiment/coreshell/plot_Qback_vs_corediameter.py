"""
===========================
Qsca vs Diameter Shell Scat
===========================

"""


def run():
    import numpy as np
    from PyMieSim.Experiment import SourceSet, Setup, CoreShellSet
    from PyMieSim.Materials import BK7, Silver
    from PyMieSim import Measure

    CoreDiameter = np.geomspace(100e-09, 600e-9, 400)
    Wavelength = [800e-9, 900e-9, 1000e-9]

    scatSet = CoreShellSet(CoreDiameter=CoreDiameter,
                           ShellDiameter=800e-9,
                           CoreMaterial=Silver,
                           ShellMaterial=BK7,
                           nMedium=1)

    sourceSet = SourceSet(Wavelength=Wavelength,
                          Polarization=0,
                          Amplitude=1)

    Experiment = Setup(scatSet, sourceSet)

    Data = Experiment.Get([Measure.Qsca, Measure.Qback])

    Data.Plot(y=Measure.Qback, x=scatSet.CoreDiameter, yScale='log').Show()


if __name__ == '__main__':
    run()
