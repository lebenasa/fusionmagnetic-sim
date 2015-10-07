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

def plotField(xmin, xmax, ymin, ymax, field, delta=0.25, level=10):
    x = np.arange(xmin, xmax, delta)
    y = np.arange(ymin, ymax, delta)
    X, Y = np.meshgrid(x, y)
    Z = field(X, Y)
    CS = plt.contour(X, Y, Z, level)
    plt.clabel(CS, fontsize=9, inline=1)

if __name__ == '__main__':
    field = AxialField()
    field.preview()