# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 03:28:03 2015

@author: leben
A script to obtain particle orbit within magnetic field with poloid gradient
using wide range of parameters.
"""
import settings
from HelixSim import Helix

def frange(start, stop, steps):
    out = []
    a = start
    while a < stop:
        out.append(a)
        a += steps
    return out

class HelixExperiment(Helix):
    def __init__(self):
        super(HelixExperiment, self).__init__()
        
    def execute(self, start=0.0, stop=1.0, steps=0.1):
        import itertools
#        alpha = frange(start, stop, steps)
        alpha = 0.2
#        beta = frange(start, stop, steps)
        beta = 0.5
        gamma = frange(start, stop, steps)
        # Don't include L and n, too long. . .
        for p in gamma:
            print 'Alpha = {a}\tBeta = {b}\tGamma = {c}'.format(a=alpha, b=beta, c=p)
            self.simulate(alpha, beta, p, 1.0, 1.0)
            self.plotSuperimposed(alpha, beta, p, 1.0, 1.0)
            try:
                raw_input('Continue?')
            except EOFError:
                print 'Bye. . .'
                return
            
    def savePlot(self, alpha, beta, gamma, L, n):
        import numpy as np
        import matplotlib.pyplot as plt
        from plot_utility import extractData
        
        s = settings.Settings()
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                R = np.hypot(np.array(x), np.array(y))
                plt.plot(z, R, '-', label=self.label(particle))
        plt.xlabel('z (m)')
        plt.ylabel('R (m)')
        plt.legend(loc=0)
        s.outext = '.png'
        plt.savefig(s.outpath())
        plt.clf()
        
if __name__ == '__main__':
    import argparse as ap
    parser = ap.ArgumentParser(description='A script to collect large ammount of data from Helix field')
    parser.add_argument('--start', default=0.0, type=float)
    parser.add_argument('--stop', default=1.0, type=float)
    parser.add_argument('--step', default=0.1, type=float)
    
    args = parser.parse_args()
    
    app = HelixExperiment()
    app.execute(args.start, args.stop, args.step)