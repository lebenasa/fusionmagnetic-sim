# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 19:39:31 2015

@author: leben
Simulate charged particle motion within magnetic field with axial gradient
"""
import numpy as np
import matplotlib.pyplot as plt
from plot_utility import extractData
import settings
import magnetic as mag
from Fields import SmoothField

class Smooth(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
#    particles = ['de+', 'tr+']
    particles = ['tr+']
#    particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Reds', 'Greens', 'Blues', 'Oranges' ]
    lmaps = [ 'red', 'green', 'blue', 'orange' ]
    style = { 'de+': 'b-', 'tr+': 'g:', 'p-': 'm-', 'e-': 'k-' }

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Smooth'
        app.x0 = 0.0
        app.y0 = 0.0
        app.z0 = 0.0
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [4.7]
        app.initialTime = 0.0
        app.timeStep = 1.0E-9
        app.endTime = 5.0E-4
#        app.endTime = 2.5E-6
        app.tolerance = 1.0E-05
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
        s = settings.Settings()
        app = mag.Application()
        
        field = SmoothField()
        field.alpha = alpha
        field.beta = beta
        field.Bz0 = app.fieldBaseStrength[0]
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha, beta)
            s.outfile = outfile
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                start = len(z) / 4 - 100
                end = len(z) / 4 + 260
#                start = 0
#                end = len(z)
                plt.plot(z[start:end], y[start:end], self.style[particle], 
                         linewidth=1, label=self.label(particle))
#                self.plotField(field, -1.6, 1.6, 0.35, 0.6)
                xmin, xmax = plt.xlim()
                ymin, ymax = plt.ylim()
                self.plotField(field, xmin, xmax, ymin, ymax)
                    
        plt.xlabel('z (m)')
        plt.ylabel('y (m)')
        plt.tight_layout()
        plt.show()
        
    def animate(self, alpha, beta, div=4, particle='tr+'):
        s = settings.Settings()
        app = mag.Application()

        field = SmoothField()
        field.alpha = alpha
        field.beta = beta
        field.Bz0 = app.fieldBaseStrength[0]
        
        outfile = self.filename(particle, alpha, beta)
        s.outfile = outfile
        with open(s.outpath()) as f:
            t, x, y, z = extractData(f, [0, 1, 2, 3])
            length = len(z) / div
            for i in xrange(div):
                start = i * length
#                if i > 0:
#                    start = (i-1) * length
#                start=0
                end = (i+1) * length
                
                if i > 0:
                    plt.plot(z[0:start], y[0:start], 'm-', alpha=0.5,
                             linewidth=0.5, label=self.label(particle))
                plt.plot(z[start:end], y[start:end], self.style[particle], 
                         linewidth=1, label=self.label(particle))
                self.plotField(field, -1.6, 1.6, 0.35, 0.6)
#                xmin, xmax = plt.xlim()
#                ymin, ymax = plt.ylim()
#                self.plotField(field, xmin, xmax, ymin, ymax)
                plt.xlabel('$z$ (m)')
                plt.ylabel('$y$ (m)')
                plt.tight_layout()
                s.outext = '_{index:03}.pdf'.format(index=i)
                plt.savefig(s.outpath())
                plt.show()
                plt.clf()
        
    # The main interest in this particular field is conveyed by the right view
    def plotField(self, field, xmin, xmax, ymin, ymax, res=1000):
        XX = np.arange(xmin, xmax, (xmax-xmin)/res)
        YY = np.arange(ymin, ymax, (ymax-ymin)/res)
        Z, Y = np.meshgrid(XX, YY)
        CS = plt.contour(Z, Y, field.zField(0.5, Y, Z), cmap='autumn_r')
        plt.clabel(CS, fontsize=9, inline=1, colors='k')

    def execute(self, alpha, beta, animate):
        self.simulate(alpha, beta)
        if animate:
            for particle in self.particles:
                self.animate(alpha, beta, particle=particle)
        else:
            self.plotSuperimposed(alpha, beta)
        
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
        '_{alpha:>02}_{beta:>02}'.format(alpha=int(alpha*10), beta=int(beta*10))

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with radial gradient')
    parser.add_argument('--alpha', default=1.0, type=float)
    parser.add_argument('--beta', default=1.0, type=float)
    parser.add_argument('--animate', action='store_true')
    
    args = parser.parse_args()
    d = Smooth()
    d.execute(args.alpha, args.beta, args.animate)
    