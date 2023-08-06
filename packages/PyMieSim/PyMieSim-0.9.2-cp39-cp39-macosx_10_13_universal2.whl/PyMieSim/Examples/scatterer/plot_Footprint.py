"""
===================
Scatterer footprint
===================

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Detector import LPmode
    from PyMieSim.Source import PlaneWave
    from PyOptik import ExpData

    Detector = LPmode(Mode="2-1", NA=0.3, sampling=200, gamma_offset=0, phi_offset=0, coupling_mode='Point')

    Source = PlaneWave(wavelength=450e-9,
                       polarization=0,
                       amplitude=1)

    Scat = Sphere(diameter=2000e-9,
                  source=Source,
                  material=ExpData('BK7'))

    footprint = Detector.get_footprint(Scat)

    footprint.Plot().Show()


if __name__ == '__main__':
    run()
