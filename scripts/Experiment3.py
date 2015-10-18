# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:27:46 2015

@author: leben
Data acquisition and processing for magnetic field with axial gradient
"""

import numpy as np
import settings
import magnetic as mag

from SineSim import Sine

class ExperimentSmooth(Sine):
    def __init__(self):
        super(ExperimentSmooth, self).__init__()
    
    def execute(self, betaStart, betaEnd, betaStep, alpha=0.5):
        beta = betaStart
        while beta < betaEnd:
            self.simulate(alpha, beta, 2.0, 1)
            beta += betaStep
            
        for particle in self.particles:
            self.calculateMirrorPoints(particle, betaStart, betaEnd, betaStep, alpha)
        
        self.plotMirrorPoints()
            
    def calculateMirrorPoints(self, particle, betaStart, betaEnd, betaStep, alpha=0.5):
        import csv
        from plot_probe import _extract
        s = settings.Settings()
        
        beta = betaStart
        mirrors = []
        while beta < betaEnd:
            s.outfile = self.filename(particle, alpha, beta, 2.0, 1)
            t, x, y, z = _extract(s.outpath())
            mirrors.append([ beta, np.max(z), np.min(z) ])
            beta += betaStep
            
        s.outfile = self.filename(particle, 0, 0, 0, 0, 'sine_mirrors_')
        with open(s.outpath(), 'w') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerows(mirrors)
            
    def plotMirrorPoints(self):
        import matplotlib.pyplot as plt
        import itertools
        from plot_utility import extractData
        
        symbols = itertools.cycle(['--bo', '--g^', '--rs'])
        
        s = settings.Settings()
        
        for particle in self.particles:
            s.outfile = self.filename(particle, 0, 0, 0, 0, 'sine_mirrors_')
            with open(s.outpath()) as f:
                beta, mx, mn = extractData(f, [0, 1, 2])
                sym = symbols.next()
                plt.plot(beta, mx, sym, markersize=8, label=self.label(particle))
                plt.plot(beta, mn, sym, markersize=8)
        plt.xlabel('$\\beta$')
        plt.ylabel('Mirror points (m)')
#        plt.legend(loc=0)
        plt.show()

if __name__ == '__main__':
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with axial gradient')
    
    parser.add_argument('--beta_start', default=0.1, type=float)
    parser.add_argument('--beta_end', default=1.1, type=float)
    parser.add_argument('--beta_step', default=0.1, type=float)
    parser.add_argument('--alpha', default=1.0, type=float)
    
    args = parser.parse_args()
    app = ExperimentSmooth()
    app.execute(args.beta_start, args.beta_end, args.beta_step, args.alpha)