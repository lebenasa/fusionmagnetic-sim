# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 21:46:30 2015

@author: leben
Simulate charged particle within poloidal magnetic field
"""
import numpy as np
import settings
import magnetic as mag

class Helix(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
    particles = ['de+' ]
#    particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Blues', 'Greens', 'Reds', 'Oranges' ]
    lmaps = [ 'blue', 'green', 'red', 'orange' ]

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Helix'
        app.x0 = 6
        app.y0 = 8
        app.z0 = 8
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [4.7, 2.0]
        app.initialTime = 0.0
        app.timeStep = 1.0E-9
        app.endTime = 1.25E-6
        app.save()
        
    def simulate(self, alpha, beta, gamma, L, n):
        app = mag.Application()
        app.fieldGradient = [ alpha, beta, gamma ]
        app.fieldLength = L
        app.fieldFreq = n
        app.save()
        s = settings.Settings()
        
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, L, n)
            s.save()
            app.particleCode = particle
            app.save()
            app.execute()
            
    def plotSuperimposed(self, alpha, beta, gamma, L, n):
        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
        from plot_utility import extractData
        
        s = settings.Settings()
        
        import itertools
        cmap = itertools.cycle(self.cmaps)
        lmap = itertools.cycle(self.lmaps)
        
        handles = []
        labels = []
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                r = np.hypot(np.array(x), np.array(y))
#                plt.plot(z, r, '-', label=self.label(particle))
                plt.scatter(z, r, c=t, cmap=cmap.next())
                handles.append(mpatches.Patch(color=lmap.next()))
                labels.append(self.label(particle))
                    
        plt.xlabel('z (m)')
        plt.ylabel('R (m)')
#        plt.legend(handles, labels, ncol=1, loc=4, framealpha=0.5)
#        plt.legend(ncol=1, loc=4, framealpha=0.5)
        plt.tight_layout()
        plt.show()
        
    def plot3d(self, alpha, beta, gamma, L, n):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from plot_utility import extractData
        
        s = settings.Settings()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                ax.plot(x, y, z)
        plt.show()
        
        
    def execute(self, alpha, beta, gamma, L, n):
        self.simulate(alpha, beta, gamma, L, n)
        self.plotSuperimposed(alpha, beta, gamma, L, n)
#        self.plot3d(alpha, beta, gamma, L, n)
#        outs = []
#        s = settings.Settings()
#        for particle in self.particles:
#            s.outfile =  self.filename(particle, alpha, beta, gamma, L, n)
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
            
    def filename(self, particle, alpha, beta, gamma, L, n, prefix='helix_'):
        return prefix + self.fileSuffix(particle) + \
        '_{alpha:>02}_{beta:>02}_{gamma:>02}_{L:>02}_{n:>02}'.format(alpha=alpha, \
        beta=beta, gamma=gamma, L=L, n=n)

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with radial gradient')
    parser.add_argument('--alpha', default=0.1, type=float)
    parser.add_argument('--beta', default=1.0, type=float)
    parser.add_argument('--gamma', default=0.9, type=float)
    parser.add_argument('--length', default=1.0, type=float)
    parser.add_argument('--freq', default=1, type=float)
    
    args = parser.parse_args()
    d = Helix()
    d.execute(args.alpha, args.beta, args.gamma, args.length, args.freq)