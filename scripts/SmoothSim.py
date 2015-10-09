# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 19:39:31 2015

@author: leben
Simulate charged particle motion within magnetic field with axial gradient
"""
import numpy as np
import settings
import magnetic as mag

class Smooth(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
#    particles = ['de+', 'tr+']
    particles = ['p-']
#    particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Reds', 'Greens', 'Blues', 'Oranges' ]
    lmaps = [ 'red', 'green', 'blue', 'orange' ]

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Smooth'
        app.x0 = 0.3
        app.y0 = 0.3
        app.z0 = 0.0
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [4.7]
        app.initialTime = 0.0
        app.timeStep = 1.0E-9
        app.endTime = 2.0E-4
        app.save()
        
    def simulate(self, alpha, beta):
        app = mag.Application()
        app.fieldGradient = [ alpha, beta ]
        app.save()
        s = settings.Settings()
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha, beta)
            s.outfile = outfile
            s.save()
            app.particleCode = particle
            app.save()
            app.execute()
            
    def plotSuperimposed(self, alpha, beta):
#        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
        from plot_utility import extractData
        
        s = settings.Settings()
#        app = mag.Application()
        
#        import itertools
#        cmap = itertools.cycle(self.cmaps)
#        lmap = itertools.cycle(self.lmaps)
#        
#        handles = []
#        labels = []
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha, beta)
            s.outfile = outfile
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
#                start = len(z) / 4 + 250
#                end = len(z) / 4 + 80
                start = 0
                end = len(z)
                plt.plot(z[start:end], y[start:end], 'r-', linewidth=1, label=self.label(particle))
#                plt.scatter(z[start:end], R[start:end], c=t[start:end], cmap=cmap.next())
#                handles.append(mpatches.Patch(color=lmap.next()))
#                labels.append(self.label(particle))
                    
        plt.xlabel('z (m)')
        plt.ylabel('y (m)')
#        plt.legend(handles, labels, ncol=1, loc=4, framealpha=0.5)
#        plt.legend(ncol=1, loc=4, framealpha=0.5)
        plt.tight_layout()
        plt.show()
        
    def execute(self, alpha, beta):
        self.simulate(alpha, beta)
        self.plotSuperimposed(alpha, beta)
        
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
            
    def filename(self, particle, alpha, beta, prefix='smooth_'):
        return prefix + self.fileSuffix(particle) + \
        '_{alpha:>02}_{beta:>02}'.format(alpha=alpha, beta=beta)

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with radial gradient')
    parser.add_argument('--alpha', default=0.5, type=float)
    parser.add_argument('--beta', default=0.2, type=float)
    
    args = parser.parse_args()
    d = Smooth()
    d.execute(args.alpha, args.beta)
    