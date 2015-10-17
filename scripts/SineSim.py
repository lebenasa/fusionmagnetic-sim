# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:28:48 2015

@author: leben
"""

import numpy as np
import settings
import magnetic as mag
from Fields import SineField

class Sine(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
#    particles = ['de+', 'tr+']
#    particles = ['de+']
    particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Reds', 'Greens', 'Blues', 'Oranges' ]
    lmaps = [ 'red', 'green', 'blue', 'orange' ]

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Sine'
        app.x0 = 0.0
        app.y0 = 0.0
        app.z0 = 0.0
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [4.7]
        app.initialTime = 0.0
        app.timeStep = 1.0E-9
        app.endTime = 1.0E-5
        app.save()
        
    def simulate(self, alpha, beta, L, n):
        app = mag.Application()
        app.fieldGradient = [ alpha, beta ]
        app.save()
        s = settings.Settings()
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha, beta, L, n)
            s.outfile = outfile
            s.save()
            app.particleCode = particle
            app.save()
            app.execute()
            
    def plotSuperimposed(self, alpha, beta, L, n):
        import matplotlib.pyplot as plt
        from plot_utility import extractData
        
        s = settings.Settings()
        field = SineField()
        field.alpha = alpha
        field.beta = beta
        field.L = L
        field.n = n
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha, beta, L, n)
            s.outfile = outfile
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
#                start = len(z) / 4 + 250
#                end = len(z) / 4 + 80
                start = 0
                end = len(z)
                plt.plot(z[start:end], y[start:end], 'r-', linewidth=1, label=self.label(particle))
                min, max = [ -1.0, 1.0 ]
                XX = np.arange(min, max, (max-min)/1000)
                YY = np.arange(min, max, (max-min)/1000)
                Z, Y = np.meshgrid(XX, YY)
                CS = plt.contour(Z, Y, field.zField(0.0, Y, Z))
                plt.clabel(CS, fontsize=9, inline=1, colors='k')
                    
        plt.xlabel('z (m)')
        plt.ylabel('y (m)')
        plt.tight_layout()
        plt.show()
        
    def execute(self, alpha, beta, L, n):
        self.simulate(alpha, beta, L, n)
        self.plotSuperimposed(alpha, beta, L, n)
        
#        s = settings.Settings()
#        outs = []
#        for particle in self.particles:
#            s.outfile =  self.filename(particle, alpha, beta)
#            outs.append(s.outpath())
#        
#        import plot_probe as pb
#        app = pb.ProberApp(outs, self.particles)
#        app.execute()
            
            
    def fileSuffix(self, particle):
        if particle == 'e-':
            return 'electron'
        elif particle == 'de+':
            return 'deuterium'
        elif particle == 'tr+':
            return 'tritium'
        elif particle == 'p-':
            return 'protide'
            
    def label(self, particle):
        if particle == 'e-':
            return '$e^-$'
        elif particle == 'de+':
            return '$De^+$'
        elif particle == 'tr+':
            return '$Tr^+$'
        elif particle == 'p-':
            return '$H^-$'
            
    def filename(self, particle, alpha, beta, L, n, prefix='smooth_'):
        return prefix + self.fileSuffix(particle) + \
        '_{alpha:>02}_{beta:>02}'.format(alpha=alpha, beta=beta)

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with radial gradient')
    parser.add_argument('--alpha', default=1.0, type=float)
    parser.add_argument('--beta', default=1.0, type=float)
    parser.add_argument('--length', '-l', default=2.0, type=float)
    parser.add_argument('--freq', '-n', default=1, type=int)
    
    args = parser.parse_args()
    d = Sine()
    d.execute(args.alpha, args.beta, args.length, args.freq)
    