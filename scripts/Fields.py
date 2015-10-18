# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 05:01:07 2015

@author: leben
A script to generate field heatmap.
"""
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt

import settings
import magnetic as mag

class RadialField(object):
    _alpha = 0.5
    _Bz0 = 4.7

    @property
    def Bz0(self):
        return self._Bz0
    @Bz0.setter
    def Bz0(self, value):
        self._Bz0 = value
       
    @property
    def alpha(self):
        return self._alpha
    @alpha.setter
    def alpha(self, value):
        self._alpha = value
    
    def zField(self, x, y):
        return self.Bz0 * ( 1 + self.alpha * ( np.hypot(x, y) ) )

class AxialField(object):
    _alpha = 0.5
    _beta = 0.5
    _Bz0 = 4.7

    @property
    def alpha(self):
        return self._alpha
    @alpha.setter
    def alpha(self, value):
        self._alpha = value
    @property
    def beta(self):
        return self._beta
    @beta.setter
    def beta(self, value):
        self._beta = value
    @property
    def Bz0(self):
        return self._Bz0
    @Bz0.setter
    def Bz0(self, value):
        self._Bz0 = value

    def rField(self, x, y):
        return -0.5 * self.Bz0 * self.beta * np.hypot(x, y)
    def zField(self, y, z, x=1.0):
        return self.Bz0 * ( 1.0 + self.alpha * np.hypot(x, y) + self.beta * z )

    def preview(self):
        plotField(-1.5, 1.5, -1.5, 1.5, self.zField)
        plt.xlabel('z')
        plt.ylabel('y')
        plt.show()
        
class SineField(object):
    Bz0 = 4.7
    alpha = 1.0
    beta = 1.0
    n = 1
    L = 1.0
    
    def zField(self, x, y, z):
        return self.Bz0 * (1 + self.alpha * np.hypot(x, y) + 
        self.beta * z * np.sin(self.n * np.pi * z / self.L))
        
    def preview(self):
        delta = 0.05
        x = 0.0
        y = np.arange(-2.0, 2.0, delta)
        z = np.arange(-2.0, 2.0, delta)
        Z, Y = np.meshgrid(z, y)
        CS = plt.contour(Z, Y, self.zField(x, Y, Z))
        plt.clabel(CS, fontsize=9, inline=1, colors='k')
        plt.show()

class TokamakField(object):
    Bz0 = 4.7
    Bteta0 = 2.0
    alpha = 1.0
    beta = 1.0
    gamma = 1.0
    eps = 1.0
    rho = 1.0
    L = 1.0
    n = 1.0
    
    def setupField(self, **kwargs):
        if 'Bz0' in kwargs:
            self.Bz0 = kwargs['Bz0']
        if 'Bteta0' in kwargs:
            self.Bteta0 = kwargs['Bteta0']
        if 'alpha' in kwargs:
            self.alpha = kwargs['alpha']
        if 'beta' in kwargs:
            self.beta = kwargs['beta']
        if 'gamma' in kwargs:
            self.gamma = kwargs['gamma']
        if 'eps' in kwargs:
            self.eps = kwargs['eps']
        if 'rho' in kwargs:
            self.rho = kwargs['rho']
        if 'L' in kwargs:
            self.L = kwargs['L']
        if 'n' in kwargs:
            self.n = kwargs['n']

    def fieldTheta(self, x, y, **kwargs):
        self.setupField(kwargs)
        return self.Bteta0 * (1 + self.rho * np.hypot(x, y))

    def fieldR(self, x, y, z, **kwargs):
        self.setupField(kwargs)
        return -1 * self.Bz0 * self.gamma * (self.n * np.pi * np.hypot(x, y) /\
            (2 * self.L)) * np.sin(self.n * self.pi * z / self.L) * \
            (1 + self.eps * np.cos(np.pi * np.arctan(y/x)))

    def zField(self, x, y, z, **kwargs):
        self.setupField(**kwargs)
        return self.Bz0 * (1 + np.hypot(self.alpha * x, self.beta* y) -\
        (self.gamma * np.cos(self.n * np.pi * z / self.L))) *\
        (1 + self.eps * np.cos(np.pi * np.arctan(y/x)))
        
    def previewZ(self, **kwargs):
        self.setupField(**kwargs)
        levels = np.arange(4.2, 8.0, 0.4)
        delta = 0.005
        x = np.arange(-0.5, 0.5, delta)
        y = 0.1
        z = np.arange(-2.0, 2.0, delta)
        Z, X = np.meshgrid(z, x)
        F = self.zField(X, y, Z)
        fig, ax = plt.subplots(2, 1, sharex=True)
        CS = ax[0].contour(Z, X, F, levels)
        plt.clabel(CS, fontsize=9, inline=1, colors='k')
        plt.ylabel = 'x'
        x = 0.1
        y = np.arange(-0.5, 0.5, delta)
        Z, Y = np.meshgrid(z, y)
        F = self.zField(x, Y, Z)
        CS = ax[1].contour(Z, Y, F, levels)
        plt.clabel(CS, fontsize=9, inline=1, colors='k')
        plt.xlabel = 'z'
        plt.ylabel = 'y'
        plt.show()

    def varyingGammaEps(self):
        g = np.arange(0.0, 0.5, 0.1)
        e = np.arange(0.0, 0.5, 0.1)

        s = settings.Settings()

        for eps in e:
            for gamma in g:
                plt.close()
                self.setupField(alpha=1.0, beta=1.0, gamma=gamma, eps=eps, rho=1.0)
                self.previewZ()
                s.outfile = 'tokamakfield_{alpha}_{beta}_{gamma}_{eps}_{rho}'.format(
                    alpha=self.alpha, beta=self.beta, gamma=self.gamma, eps=self.eps, rho=self.rho)
                s.outext = '.png'
                plt.savefig(s.outpath())

    def varyingAlphaBeta(self):
        a = np.arange(0.0, 1.1, 0.1)
        b = np.arange(0.0, 1.1, 0.1)

        s = settings.Settings()

        import itertools
        from os import path, mkdir
        s.outdir = path.join(s.outdir, 'TokamakField_alpha_beta')
        if not path.exists(s.outdir):
            mkdir(s.outdir)
        for alpha, beta in itertools.product(a, b):
            self.setupField(alpha=alpha, beta=beta, gamma=0.2, eps=0.2, rho=1.0)
            self.previewZ()
            s.outfile = 'tokamakfield_{alpha}_{beta}_{gamma}_{eps}_{rho}'.format(
                alpha=self.alpha, beta=self.beta, gamma=self.gamma, eps=self.eps, rho=self.rho)
            s.outext = '.png'
            plt.savefig(s.outpath())           
            plt.close()
    
def plotField(xmin, xmax, ymin, ymax, field, delta=0.25, level=10):
    x = np.arange(xmin, xmax, delta)
    y = np.arange(ymin, ymax, delta)
    X, Y = np.meshgrid(x, y)
    Z = field(X, Y)
    CS = plt.contour(X, Y, Z, level)
    plt.clabel(CS, fontsize=9, inline=1)

if __name__ == '__main__':
#    field = TokamakField()
#    field.previewZ(gamma=0.2, eps=0.2)
#    field.varyingGammaEps()
    field = SineField()
    field.alpha = 1.0
    field.beta = 1.0
    field.L = 2.0
    field.preview()
