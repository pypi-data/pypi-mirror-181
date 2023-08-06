"""
======================
Far-Fields computation
======================

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    Source = PlaneWave(wavelength=1000e-9,
                       polarization=0,
                       amplitude=1)

    Scat = Sphere(diameter=1500e-9,
                  source=Source,
                  index=1.4)

    Fields = Scat.get_far_field(Num=300)

    Fields.Plot().Show()


if __name__ == '__main__':
    run()
