"""
===============
SPF computation
===============

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    Source = PlaneWave(wavelength=500e-9,
                       polarization=0,
                       amplitude=1)

    Scat = Sphere(diameter=1200e-9,
                  source=Source,
                  index=1.4,
                  n_medium=1.0)

    SPF = Scat.get_spf(Num=300)

    SPF.Plot().Show()


if __name__ == '__main__':
    run()
