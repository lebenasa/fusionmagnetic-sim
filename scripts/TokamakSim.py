# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 05:39:47 2015

@author: leben
Simulate charged particle motion within Tokamak-alike magnetic field
"""
import numpy as np
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
        app.y0 = 0.2
        app.z0 = 0.4
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [4.7, 2.0]
        app.initialTime = 0.0
        app.timeStep = 1.0E-9
        app.endTime = 1E-5
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
        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from plot_utility import extractData
        
        s = settings.Settings()
        fig, ax = plt.subplots(2, 2)
        front, top, right, _ = np.ravel(ax)

        field = Fields.TokamakField()
        field.setupField(alpha=alpha, beta=beta, gamma=gamma, eps=eps, rho=rho, L=L, n=n)
        
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, eps, rho, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                front.plot(x, y, '-', label=self.label(particle))
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
                top.plot(z, y, '-', label=self.label(particle))
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
                right.plot(z, x, '-', label=self.label(particle))
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
        
    def plot3d(self, alpha, beta, gamma, eps, rho, L, n):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from plot_utility import extractData
        
        s = settings.Settings()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha, beta, gamma, eps, rho, L, n)
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                ax.plot(x, y, z)
        plt.show()
        
        
    def execute(self, alpha, beta, gamma, eps, rho, L, n):
        self.simulate(alpha, beta, gamma, eps, rho, L, n)
        self.plotSuperimposed(alpha, beta, gamma, eps, rho, L, n)
            
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
            
    def filename(self, particle, alpha, beta, gamma, eps, rho, L, n, prefix='tokamak_'):
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
    
    args = parser.parse_args()
    d = Tokamak()
    d.execute(args.alpha, args.beta, args.gamma,args.eps, args.rho, args.length, args.freq)