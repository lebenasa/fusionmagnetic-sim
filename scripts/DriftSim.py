# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 10:59:47 2015

@author: leben
Simulate magnetic field with radial gradient
"""
import numpy as np
import matplotlib.pyplot as plt
from plot_utility import extractData

import settings
import magnetic as mag
from Fields import RadialField

class Drift(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
    particles = ['tr+']
    #particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Blues', 'Greens', 'Reds', 'Oranges' ]
    lmaps = [ 'blue', 'green', 'red', 'orange' ]
    
    style = { 'de+': 'b-', 'tr+': 'g:', 'p-': 'r-', 'e-': 'k-' }

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Drift'
        app.x0 = 0.01
        app.y0 = 0.01
        app.z0 = 0
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        #app.vx0 = 1.0E5 * np.cos(np.pi / 4)
        #app.vy0 = 1.0E5 * np.sin(np.pi / 4)
        #app.vz0 = 1.0E5
        app.fieldBaseStrength = [0.0, 0.0, 4.7]
        app.initialTime = 0.0
        app.timeStep = 1.0E-10
        app.endTime = 2.5E-5
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
        s = settings.Settings()
        app = mag.Application()

        field = RadialField()
        field.alpha = alpha
        field.Bz0 = app.fieldBaseStrength[2]
        
        for particle in self.particles:
            outfile = self.filename(particle, alpha)
            s.outfile = outfile
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                plt.plot(x, y, self.style[particle], label=self.label(particle))
                xmin, xmax = [ -0.03, 0.03 ]
                ymin, ymax = [ -0.03, 0.03 ]
                self.plotField(field, xmin, xmax, ymin, ymax)
                plt.xlabel('$z$ (m)')
                plt.ylabel('$y$ (m)')
                plt.tight_layout()
                plt.show()
                
    def animate(self, alpha, div=4, particle='tr+'):
        s = settings.Settings()
        app = mag.Application()

        field = RadialField()
        field.alpha = alpha
        field.Bz0 = app.fieldBaseStrength[2]
        
        outfile = self.filename(particle, alpha)
        s.outfile = outfile
        with open(s.outpath()) as f:
            t, x, y, z = extractData(f, [0, 1, 2, 3])
            length = len(z) / div
            for i in xrange(div):
#                start = i * length
#                if i > 0:
#                    start = (i) * length
                start=0
                end = (i+1) * length
                
                # Plot front view, no real way to refactor these *sigh*
                plt.plot(x[start:end], y[start:end], self.style[particle], 
                         linewidth=1, label=self.label(particle))
                xmin, xmax = [ -0.03, 0.03 ]
                ymin, ymax = [ -0.03, 0.03 ]
                self.plotField(field, xmin, xmax, ymin, ymax, orientation='front')
                plt.xlabel('$x$ (m)')
                plt.ylabel('$y$ (m)')
                plt.tight_layout()
                s.outext = '_long_front_{index:03}.pdf'.format(index=i)
                plt.savefig(s.outpath())
                plt.show()
                plt.clf()
                
                # Plot right view, no real way to refactor these *sigh*
                plt.plot(z[start:end], y[start:end], self.style[particle], 
                         linewidth=1, label=self.label(particle))
                xmin, xmax = [ 0.0, 25 ]
                ymin, ymax = [ -0.03, 0.03 ]
                self.plotField(field, xmin, xmax, ymin, ymax, orientation='right')
                plt.xlabel('$z$ (m)')
                plt.ylabel('$y$ (m)')
                plt.tight_layout()
                s.outext = '_long_right_{index:03}.pdf'.format(index=i)
                plt.savefig(s.outpath())
                plt.show()
                plt.clf()
                                
    def plotField(self, field, xmin, xmax, ymin, ymax, res=1000, orientation='front'):
        XX = np.arange(xmin, xmax, (xmax-xmin)/res)
        YY = np.arange(ymin, ymax, (ymax-ymin)/res)
        if orientation == 'front':
            X, Y = np.meshgrid(XX, YY)
            CS = plt.contour(X, Y, field.zField(X, Y), cmap='autumn_r')
            plt.clabel(CS, fontsize=9, inline=1, colors='k')
        elif orientation == 'right':
            Z, Y = np.meshgrid(XX, YY)
            CS = plt.contour(Z, Y, field.zField(0.0, Y), cmap='autumn_r')
#            plt.clabel(CS, fontsize=9, inline=1, colors='k')
        
    def execute(self, alpha, animate):
        self.simulate(alpha)
        if animate:
            for particle in self.particles:
                self.animate(alpha, div=8, particle=particle)
        else:
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
        return prefix + self.fileSuffix(particle) + '_{alpha:>02}'.format(alpha=int(alpha * 10))

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with radial gradient')
    parser.add_argument('--alpha', default=0.5, type=float)
    parser.add_argument('--animate', action='store_true')
    
    args = parser.parse_args()
    d = Drift()
    d.execute(args.alpha, args.animate)
    
