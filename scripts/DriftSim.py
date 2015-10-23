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
    particles = ['de+']
    #particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Blues', 'Greens', 'Reds', 'Oranges' ]
    lmaps = [ 'blue', 'green', 'red', 'orange' ]

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Drift'
        app.x0 = 0.0
        app.y0 = 0.0
        app.z0 = 0
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        #app.vx0 = 1.0E5 * np.cos(np.pi / 4)
        #app.vy0 = 1.0E5 * np.sin(np.pi / 4)
        #app.vz0 = 1.0E5
        app.fieldBaseStrength = [0.0, 0.0, 4.7]
        app.initialTime = 0.0
        app.timeStep = 1.0E-10
        app.endTime = 5.0E-5
        app.tolerance = 1.0E-12
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
            app.save()
            app.execute()
            
    def plotSuperimposed(self, alpha):
        import matplotlib.pyplot as plt
        from plot_utility import extractData
        
        s = settings.Settings()
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha)
            s.outfile = outfile
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                plt.plot(z, y, '-', label=self.label(particle))
                    
        plt.xlabel('z (m)')
        plt.ylabel('y (m)')
        plt.tight_layout()
        plt.show()
        
    def execute(self, alpha):
        self.simulate(alpha)
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
    