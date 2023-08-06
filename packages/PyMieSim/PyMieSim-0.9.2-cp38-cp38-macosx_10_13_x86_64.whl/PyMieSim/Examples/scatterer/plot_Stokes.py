"""
=============================
Stokes parameters computation
=============================

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    Source = PlaneWave(wavelength=450e-9,
                       polarization=0,
                       amplitude=1)

    Scat = Sphere(diameter=300e-9,
                  source=Source,
                  index=1.4)

    Stokes = Scat.get_stokes(Num=100)

    Stokes.Plot().Show()


if __name__ == '__main__':
    run()
