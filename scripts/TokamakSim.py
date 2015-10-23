# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 05:39:47 2015

@author: leben
Simulate charged particle motion within Tokamak-alike magnetic field
"""
import numpy as np
import matplotlib.pyplot as plt
from plot_utility import extractData
        
import settings
import magnetic as mag
import Fields

class Tokamak(object):    
#    particles = [ 'e-', 'de+', 'tr+', 'p-' ]
    particles = ['de+' ]
#    particles = [ 'de+', 'tr+', 'p-' ]
    cmaps = [ 'Blues', 'Greens', 'Reds', 'Oranges' ]
    lmaps = [ 'blue', 'green', 'red', 'orange' ]

    def __init__(self):
        app = mag.Application()
        app.fieldCode = 'Tokamak'
        app.x0 = 0.1
        app.y0 = 0.1
        app.z0 = 0.005
        app.useKineticEnergy = True
        app.kineticEnergy = 1
        #app.useKineticEnergy = False
        #app.vx0 = 1.0E06
        #app.vy0 = 1.0E06
        #app.vz0 = 1.0E07
        app.fieldBaseStrength = [4.7, 4.7]
        app.initialTime = 0.0
        app.timeStep = 1.0E-9
        app.endTime = 1.0E-5
        app.save()
        
    def simulate(self, alpha, beta, gamma, eps, rho, L, n):
        app = mag.Application()
        app.fieldGradient = [ alpha, beta, gamma, eps, rho ]
        app.fieldLength = L
        app.fieldFreq = n
        app.save()
        s = settings.Settings()
        
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, eps, rho, L, n)
            s.save()
            app.particleCode = particle
            app.save()
            app.execute()
            
    def plotSuperimposed(self, alpha, beta, gamma, eps, rho, L, n):
        s = settings.Settings()
        fig, ax = plt.subplots(2, 2)
        right, front, top, _ = np.ravel(ax)

        field = Fields.TokamakField()
        field.setupField(alpha=alpha, beta=beta, gamma=gamma, eps=eps, rho=rho, L=L, n=n)
        
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, eps, rho, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                front.plot(x, y, '-g', label=self.label(particle))
                front.set_xlabel('x')
                front.set_ylabel('y')
                #min, max = front.get_xlim()
                min, max = [-0.5, 0.5]
                levels = np.arange(4.2, 6.3, 0.4)
                XX = np.arange(min, max, (max-min)/100)
                #min, max = front.get_ylim()
                YY = np.arange(min, max, (max-min)/100)
                X, Y = np.meshgrid(XX, YY)
                Z = 0.1
                F = field.zField(X, Y, Z)
                CS = front.contour(X, Y, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
                top.plot(z, y, '-g', label=self.label(particle))
                top.set_xlabel('z')
                top.set_ylabel('y')
                #min, max = top.get_xlim()
                min, max = [-2.0, 2.0]
                ZZ = np.arange(min, max, (max-min)/100)
                #min, max = top.get_ylim()
                min, max = [-0.5, 0.5]
                YY = np.arange(min, max, (max-min)/100)
                Z, Y = np.meshgrid(ZZ, YY)
                X = 0.1
                F = field.zField(X, Y, Z)
                CS = top.contour(Z, Y, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
                right.plot(z, x, '-g', label=self.label(particle))
                right.set_xlabel('z')
                right.set_ylabel('x')
                #min, max = right.get_xlim()
                min, max = [-2.0, 2.0]
                ZZ = np.arange(min, max, (max-min)/100)
                #min, max = right.get_ylim()
                min, max = [-0.5, 0.5]
                XX = np.arange(min, max, (max-min)/100)
                Z, X = np.meshgrid(ZZ, XX)
                Y = 0.1
                F = field.zField(X, Y, Z)
                CS = right.contour(Z, X, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
        plt.tight_layout()
        plt.show()
             
    def plotSuperimposed2(self, alpha, beta, gamma, eps, rho, L, n):
        from mpl_toolkits.mplot3d import Axes3D
        
        s = settings.Settings()

        field = Fields.TokamakField()
        field.setupField(alpha=alpha, beta=beta, gamma=gamma, eps=eps, rho=rho, L=L, n=n)

        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, eps, rho, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                plt.plot(x, y, '-b', label=self.label(particle))
                plt.xlabel('x')
                plt.ylabel('y')
                #min, max = front.get_xlim()
                min, max = [-0.5, 0.5]
                levels = np.arange(4.2, 6.3, 0.4)
                XX = np.arange(min, max, (max-min)/1000)
                #min, max = front.get_ylim()
                YY = np.arange(min, max, (max-min)/1000)
                X, Y = np.meshgrid(XX, YY)
                Z = 0.1
                F = field.zField(X, Y, Z)
                CS = plt.contour(X, Y, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
                plt.show()
                plt.close()
                plt.plot(z, y, '-b', label=self.label(particle))
                plt.xlabel('z')
                plt.ylabel('y')
                #min, max = top.get_xlim()
                min, max = [-2.0, 2.0]
                ZZ = np.arange(min, max, (max-min)/1000)
                #min, max = top.get_ylim()
                min, max = [-0.5, 0.5]
                YY = np.arange(min, max, (max-min)/1000)
                Z, Y = np.meshgrid(ZZ, YY)
                X = 0.1
                F = field.zField(X, Y, Z)
                CS = plt.contour(Z, Y, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
                plt.show()
                plt.close()
                plt.plot(z, x, '-b', label=self.label(particle))
                plt.xlabel('z')
                plt.ylabel('x')
                #min, max = right.get_xlim()
                min, max = [-2.0, 2.0]
                ZZ = np.arange(min, max, (max-min)/1000)
                #min, max = right.get_ylim()
                min, max = [-0.5, 0.5]
                XX = np.arange(min, max, (max-min)/1000)
                Z, X = np.meshgrid(ZZ, XX)
                Y = 0.1
                F = field.zField(X, Y, Z)
                CS = plt.contour(Z, X, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
                plt.show()
        
    def plot3d(self, alpha, beta, gamma, eps, rho, L, n):
        from mpl_toolkits.mplot3d import Axes3D
        
        s = settings.Settings()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, eps, rho, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                ax.plot(x, y, z)
        plt.show()
        
    def animate(self, alpha, beta, gamma, eps, rho, L, n, div=32, particle='de+'):
        field = Fields.TokamakField()
        field.setupField(alpha=alpha, beta=beta, gamma=gamma, eps=eps, rho=rho, L=L, n=n)

        s = settings.Settings()
        s.outfile = self.filename(particle, alpha, beta, gamma, eps, rho, L, n)
        with open(s.outpath()) as f:
            t, x, y, z = extractData(f, [0, 1, 2, 3])
            length = len(z) / div
            for i in xrange(div):
                start = i * length
                if i > 0:
                    start = (i-1) * length
                end = (i+1) * length
                plt.subplot(121)
                plt.plot(x[start:end], y[start:end], '-b', label=self.label(particle))
                plt.xlabel('x')
                plt.ylabel('y')
                min, max = [-0.5, 0.5]
                levels = np.arange(4.2, 6.3, 0.4)
                XX = np.arange(min, max, (max-min)/1000)
                YY = np.arange(min, max, (max-min)/1000)
                X, Y = np.meshgrid(XX, YY)
                Z = 0.1
                F = field.zField(X, Y, Z)
                CS = plt.contour(X, Y, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
                plt.subplot(122)
                plt.plot(z[start:end], y[start:end], '-b', label=self.label(particle))
                plt.xlabel('z')
                plt.ylabel('y')
                min, max = [-2.2, 2.0]
                ZZ = np.arange(min, max, (max-min)/1000)
                min, max = [-0.5, 0.5]
                YY = np.arange(min, max, (max-min)/1000)
                Z, Y = np.meshgrid(ZZ, YY)
                X = 0.1
                F = field.zField(X, Y, Z)
                CS = plt.contour(Z, Y, F, levels)
                plt.clabel(CS, fontsize=9, colors='k', inline=1)
                s.outext = '_{index:03}.png'.format(index=i)
                plt.savefig(s.outpath())
                plt.clf()

    def execute(self, alpha, beta, gamma, eps, rho, L, n, animate):
        self.simulate(alpha, beta, gamma, eps, rho, L, n)
        if animate:
            self.animate(alpha, beta, gamma, eps, rho, L, n)
        else:
            self.plotSuperimposed2(alpha, beta, gamma, eps, rho, L, n)
            
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
            
    def filename(self, particle, alpha, beta, gamma, eps, rho, L, n, prefix='tokamak_banana_'):
        return prefix + self.fileSuffix(particle) + \
        '_{alpha:>02}_{beta:>02}_{gamma:>02}_{eps:>02}_{rho:>02}_{L:>02}_{n:>02}'.format(alpha=alpha, \
        beta=beta, gamma=gamma, eps=eps, rho=rho, L=L, n=n)

if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with tokamak-like shape')
    parser.add_argument('--alpha', default=1.0, type=float)
    parser.add_argument('--beta', default=1.0, type=float)
    parser.add_argument('--gamma', default=0.2, type=float)
    parser.add_argument('--eps', default=0.2, type=float)
    parser.add_argument('--rho', default=1.0, type=float)
    parser.add_argument('--length', default=1.0, type=float)
    parser.add_argument('--freq', default=1, type=float)
    parser.add_argument('--animate', action='store_true')
    
    args = parser.parse_args()
    d = Tokamak()
    d.execute(args.alpha, args.beta, args.gamma,args.eps, args.rho, args.length, args.freq, args.animate)
