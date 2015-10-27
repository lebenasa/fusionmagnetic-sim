# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:28:48 2015

@author: leben
"""

import numpy as np
import matplotlib.pyplot as plt
from plot_utility import extractData
        
import settings
import magnetic as mag
from Fields import SineField

class Sine(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
#    particles = ['de+', 'tr+']
    particles = ['e-']
    #particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Reds', 'Greens', 'Blues', 'Oranges' ]
    lmaps = [ 'red', 'green', 'blue', 'orange' ]
    style = { 'de+': 'b-', 'tr+': 'g:', 'p-': 'm-', 'e-': 'k-' }

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Sine'
        app.x0 = 0.2
        app.y0 = 0.2
        app.z0 = 0.0
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [4.7]
        app.initialTime = 0.0
        app.timeStep = 1.0E-9
        app.endTime = 5.1E-8
        app.tolerance = 1.0E-5
        app.save()
        
    def simulate(self, alpha, beta, L, n):
        app = mag.Application()
        app.fieldGradient = [ alpha, beta ]
        app.fieldLength = L
        app.fieldFreq = n
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
                #start = len(z) / 4 + 250
                #end = len(z) / 4 + 180
                start = 0
                end = len(z)
                plt.plot(z[start:end], y[start:end], self.style[particle], 
                         linewidth=1, label=self.label(particle))
        xmin, xmax = [ -0.4, 0.4 ]
        ymin, ymax = [ 0.1, 0.3 ]
#        xmin, xmax = plt.xlim()
#        ymin, ymax = plt.ylim()
        self.plotField(field, xmin, xmax, ymin, ymax)
                    
        plt.xlabel('$z$ (m)')
        plt.ylabel('$y$ (m)')
#        plt.text(0.25, 0.8, r'$B_z = B_{z0} \left( 1 + \alpha r + \beta z\ \sin (\frac{n \pi z}{L}) \right)$',
#                 fontsize=15)
#        plt.text(0.25, 0.7, '$\\alpha = {alp},\\ \\beta = {beta}$'.format(alp=alpha, beta=beta),
#                 fontsize=15)
        plt.tight_layout()
        s.outext = '.pdf'
        plt.savefig(s.outpath())
        plt.show()

    def animate(self, alpha, beta, L, n, div=32, particle='de+'):
        s = settings.Settings()
        field = SineField()
        field.alpha = alpha
        field.beta = beta
        field.L = L
        field.n = n
        
        outfile = self.filename(particle, alpha, beta, L, n)
        s.outfile = outfile
        with open(s.outpath()) as f:
            t, x, y, z = extractData(f, [0, 1, 2, 3])
            length = len(z) / div
            for i in xrange(div):
                start = i * length
                if i > 0:
                    start = (i-1) * length
                end = (i+1) * length
                plt.plot(z[start:end], y[start:end], 'b-', linewidth=1, label=self.label(particle))
                xmin, xmax = [ -1.15, 1.15 ]
                ymin, ymax = [ -1.0, 1.0 ]
                self.plotField(field, xmin, xmax, ymin, ymax)
                plt.xlabel('$z$ (m)')
                plt.ylabel('$y$ (m)')
                plt.tight_layout()
                s.outext = '_{index:03}.png'.format(index=i)
                plt.text(0.25, 0.8, r'$B_z = B_{z0} \left( 1 + \alpha r + \beta z\ \sin (\frac{n \pi z}{L}) \right)$',
                         fontsize=15)
                plt.text(0.25, 0.7, '$\\alpha = {alp},\\ \\beta = {beta}$'.format(alp=alpha, beta=beta),
                         fontsize=15)
                plt.savefig(s.outpath())
                plt.clf()

    def plotField(self, field, xmin, xmax, ymin, ymax, res=1000):
        XX = np.arange(xmin, xmax, (xmax-xmin)/res)
        YY = np.arange(ymin, ymax, (ymax-ymin)/res)
        Z, Y = np.meshgrid(XX, YY)
        CS = plt.contour(Z, Y, field.zField(0.0, Y, Z), cmap='autumn_r')
        plt.clabel(CS, fontsize=9, inline=1, colors='k')
        
    def execute(self, alpha, beta, L, n, animate):
        self.simulate(alpha, beta, L, n)
        if animate:
            self.animate(alpha, beta, L, n)
        else:
            self.plotSuperimposed(alpha, beta, L, n)
            
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
            
    def filename(self, particle, alpha, beta, L, n, prefix='sine_'):
        return prefix + self.fileSuffix(particle) + \
        '_{alpha:>02}_{beta:>02}'.format(alpha=int(alpha*10), beta=int(beta*10))

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with sine axial gradient')
    parser.add_argument('--alpha', '-a', default=1.0, type=float)
    parser.add_argument('--beta', '-b', default=1.0, type=float)
    parser.add_argument('--length', '-l', default=1.0, type=float)
    parser.add_argument('--freq', '-n', default=1, type=int)
    parser.add_argument('--animate', action='store_true')
    
    args = parser.parse_args()
    d = Sine()
    d.execute(args.alpha, args.beta, args.length, args.freq, args.animate)
    