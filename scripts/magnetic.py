# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 03:53:57 2015

@author: Leben Asa

Main script: provide simple text interface to change settings and run
simulation.
"""

import os
import argparse
from settings import Settings, Simulator
from utility import formats

class Application(Simulator):
    """Application class
    In addition of Simulator features, this class has __execute__ method to
    run the simulation using stored parameters. It doesn't call save when
    destroyed, however (since JSON files are used for easy parameters sync bet-
    ween scripts).
    """

    def execute(self):
        import datetime as dt
        import subprocess as sp
        s = Settings()
        appin = ' '.join(self.serialize())

        if os.path.exists(s.outdir) is False:
            os.mkdir(s.outdir)

        outfull = os.path.join(s.outdir, s.outfile)
        if s.appendDateToOutFile:
            outfull += dt.datetime.now().strftime('.%d.%m.%Y.%H.%M.%S.%f')
        outfull += s.outext

        with open(outfull, 'w') as out:
            process = sp.Popen([s.app], stdout=out, stderr=sp.PIPE,
                               stdin=sp.PIPE, cwd=s.root)
            stdout, stderr = process.communicate(appin)
            print stderr


descstr = """
Text interface to setup and run charged particle motion simulation.
This script retains previous settings and parameters, for example:
    $> python ./magnetic.py --r0 0.0 0.0 0.0 --base 0.0 0.0 4.7 -h 1.0E-09
will run simulation with initial position (0.0, 0.0, 0.0) and magnetic field \
base vector (0.0, 0.0, 4.7) using timestep 1.0E-09 seconds. Suppose the \
timestep was too small, on second run:
    $> python ./magnetic.py -h 1.0E-08
will run simulation with different timestep while other parameters stay same.\

NOTE:
Timestep h is used as fixed step or first trial of adaptive step driver \
depending on simulator build.
"""[1:-1]

mainstr = """
========================================================
Charged Particle Motion within Magnetic Field Simulation
========================================================


"""[1:-1].format(**formats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=descstr)
    # parser.add_argument('--lastrun' )
    pass
