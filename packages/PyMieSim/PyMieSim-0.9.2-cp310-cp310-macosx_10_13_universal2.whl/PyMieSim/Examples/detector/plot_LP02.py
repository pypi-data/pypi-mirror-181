"""

LP02 Mode detector
==================

"""


def run():
    from PyMieSim.Detector import LPmode

    Detector = LPmode(Mode="0-2",
                      rotation=0.,
                      sampling=300,
                      NA=0.3,
                      gamma_offset=30,
                      phi_offset=0,
                      coupling_mode='Point')

    Detector.Plot().Show()


if __name__ == '__main__':
    run()
