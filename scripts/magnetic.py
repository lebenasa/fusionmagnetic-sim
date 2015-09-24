# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 03:53:57 2015

@author: Leben Asa

Main script: provide simple text interface to change settings and run
simulation.
"""

import argparse
from settings import Settings
from utility import formats

settings = Settings()

descstr = """
Text interface to setup and run charged particle motion simulation.
This script retains previous settings and parameters, for example:
    $> python ./magnetic.py --r0 0.0 0.0 0.0 --base 0.0 0.0 4.7 -h 1.0E-09
will run simulation with initial position (0.0, 0.0, 0.0) and magnetic field \
base vector (0.0, 0.0, 4.7) using timestep 1.0E-09 seconds. Suppose the \
timestep was too small, on second run:
    $> python ./magnetic.py -h 1.0E-08
will run simulation with different timestep while other parameters stay same.\
"""[1:-1]

mainstr = """
========================================================
Charged Particle Motion within Magnetic Field Simulation
========================================================


"""[1:-1].format(**formats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=descstr)
    parser.add_argument('--lastrun', )
    pass
