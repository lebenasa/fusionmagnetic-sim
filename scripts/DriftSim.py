# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 10:59:47 2015

@author: leben
Simulate magnetic field with radial gradient
"""
import numpy as np
import settings
import magnetic as mag

class Drift(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
#    particles = ['de+']
    particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Blues', 'Greens', 'Reds', 'Oranges' ]
    lmaps = [ 'blue', 'green', 'red', 'orange' ]

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Drift'
        app.x0 = 0.3
        app.y0 = 0.3
        app.z0 = 0
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [0.0, 0.0, 4.7]
        app.initialTime = 1.0E-03
        app.timeStep = 1.0E-9
        app.endTime = 2.0E-3
        app.save()
        
    def simulate(self, alpha):
        app = mag.Application()
        app.fieldGradient = [ alpha ]
        app.save()
        s = settings.Settings()
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha)
            s.outfile = outfile
            s.save()
            app.particleCode = particle
            app.useKineticEnergy = False
            if particle == 'de+':
                app.x0 = 1.404074
                app.y0 = -1.92602e-01
                app.z0 = 1.19896e+03
                app.vx0 = 2.45512e+06
                app.vy0 = 3.89723e+06
                app.vz0 = 1.19896e+06
            elif particle == 'tr+':
                app.x0 = 5.52679e-01
                app.y0 = -1.03044e+00
                app.z0 = 9.79730e+02
                app.vx0 = -2.59609e+06
                app.vy0 = -5.38724e+05
                app.vz0 = 9.79730e+05
            elif particle == 'p-':
                app.x0 = -2.07641e+00
                app.y0 = -2.78223e+00 
                app.z0 = 1.70132e+03 
                app.vx0 = -1.09751e+07 
                app.vy0 = -2.23460e+07 
                app.vz0 = 1.70132e+06
            app.save()
            app.execute()
            
    def plotSuperimposed(self, alpha):
#        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
        from plot_utility import extractData
        
        s = settings.Settings()
        
#        import itertools
#        cmap = itertools.cycle(self.cmaps)
#        lmap = itertools.cycle(self.lmaps)
        
#        handles = []
#        labels = []
        for particle in self.particles:
            outfile = self.filename(particle, alpha)
            s.outfile = outfile
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
#                r = np.hypot(np.array(x), np.array(y))
                plt.plot(z, y, ',', label=self.label(particle))
#                plt.scatter(z, r, c=t, cmap=cmap.next())
#                handles.append(mpatches.Patch(color=lmap.next()))
#                labels.append(self.label(particle))
                    
        plt.xlabel('z (m)')
        plt.ylabel('y (m)')
#        plt.legend(handles, labels, ncol=1, loc=4, framealpha=0.5)
#        plt.legend(ncol=1, loc=4, framealpha=0.5)
        plt.tight_layout()
        plt.show()
        
    def execute(self, alpha):
#        self.simulate(alpha)
        self.plotSuperimposed(alpha)
            
            
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
            
    def filename(self, particle, alpha, prefix='drift2_'):
        return prefix + self.fileSuffix(particle) + '_{alpha:>02}'.format(alpha=alpha)

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with radial gradient')
    parser.add_argument('--alpha', default=0.5, type=float)
    
    args = parser.parse_args()
    d = Drift()
    d.execute(args.alpha)
    