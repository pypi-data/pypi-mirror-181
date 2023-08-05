"""

LP11 Mode detector
==================

"""


def run():
    from PyMieSim.Detector import LPmode

    Detector = LPmode(Mode="1-1",
                      Rotation=0.,
                      Sampling=300,
                      NA=0.3,
                      GammaOffset=0,
                      PhiOffset=40,
                      CouplingMode='Point')

    Detector.Plot().Show()


if __name__ == '__main__':
    run()
