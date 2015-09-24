# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:45:44 2015

@author: leben

Testing program build
===

A note about tests
---

This project was made by using test driven approach. The tests were carried in
another repository, thus optimizing this repository for release.
This script merely tests whether the scripts system can find and execute the
program.
"""

import os
import subprocess as sp
from settings import Settings
import utility as ut

def testRun():
    settings = Settings()
    app = settings.app
    tmp = settings.outdir
    tmpout = os.path.join(tmp, "tmpresult.csv")

    heretext = """
    de+             # Particle codename
    0.0 0.0 0.0     # Initial position (m)
    Y               # Y: Initial velocity in keV instead of m/s
    15              # Plasma temperature (keV)
    # n             # Another example
    # 1.0 1.0 1.0   # Initial velocity (m/s)
    Homogen         # Magnetic field codename
    4.7 0.0 0.0     # Magnetic field strength (Tesla)
    0.0             # Initial time (s)
    1.0E-04         # End time (s)
    1.0E-09         # Timestep (s)
    """[1:-1]
    
    params = " ".join(ut.exclude(heretext))
    if os.path.exists(tmp) is False:
        os.mkdir(tmp)
    
    with open(tmpout, 'w') as out:
        process = sp.Popen([app], stdout=out, stderr=sp.PIPE, stdin=sp.PIPE, cwd=tmp)
        stdout, stderr = process.communicate(params)
        print stderr
        
    success = False
    with open(tmpout, 'r') as out:
        for line in out:
            pass
        success = line.find("END OUTPUT") != -1
    return success

if __name__ == '__main__':
    print testRun()