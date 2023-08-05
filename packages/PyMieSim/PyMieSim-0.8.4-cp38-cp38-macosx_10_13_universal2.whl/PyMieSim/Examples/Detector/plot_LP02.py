"""

LP02 Mode detector
==================

"""


def run():
    from PyMieSim.Detector import LPmode

    Detector = LPmode(Mode="0-2",
                      Rotation=0.,
                      Sampling=300,
                      NA=0.3,
                      GammaOffset=30,
                      PhiOffset=0,
                      CouplingMode='Point')

    Detector.Plot().Show()


if __name__ == '__main__':
    run()
