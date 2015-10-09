# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 19:59:39 2015

@author: leben
Utility script to plot a part of output data
"""
import curses
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from plot_utility import extractData

def _extract(filename):
    with open(filename) as f:
        t, x, y, z = extractData(f, [0, 1, 2, 3])
        t = np.array(t)
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
    return [t, x, y, z]
    
class ProberApp(object):
    start = 0
    length = 100
    x = []
    y = []
    z = []
    t = []
    particles = []
    
    cmaps = [ 'Reds', 'Greens', 'Blues', 'Oranges' ]
    lmaps = [ 'red', 'green', 'blue', 'orange' ]
    
    def __init__(self, filenames, particles):
        for fn in filenames:
            a, b, c, d = _extract(fn)
            self.t.append(a)
            self.x.append(b)
            self.y.append(c)
            self.z.append(d)
        self.particles = particles
        self.maxl = len(self.t[0])
        
    def __del__(self):
        pass
        
    def execute(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        plt.xlabel('z (m)')
        plt.ylabel('R (m)')
        plt.tight_layout()
        plt.ion()
        self.plotProbe()
        plt.show()
        while True:
            self.plotProbe()
            c = self.stdscr.getch()
            if c == curses.KEY_UP:
                if self.start >= 0:
                    self.start -= 1
            elif c == curses.KEY_DOWN:
                if self.start + 1 < self.maxl:
                    self.start += 1
            elif c == curses.KEY_NPAGE:
                if self.start - self.length > 0:
                    self.start -= self.length
                else:
                    self.start = 0
            elif c == curses.KEY_PPAGE:
                if self.start + self.length < self.maxl:
                    self.start += self.length
                else:
                    self.start = self.maxl - self.length - 1
            elif c == ord('.'):
                self.length += 1
            elif c == ord(','):
                self.length -= 1
            elif c == ord('>'):
                self.length *= 10
            elif c == ord('<'):
                self.length /= 10
            elif c == ord('q'):
                break
            else:
                continue
                    
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
            
    def plotProbe(self):
        import matplotlib.patches as mpatches
        import itertools
        cmap = itertools.cycle(self.cmaps)
        lmap = itertools.cycle(self.lmaps)
        
        plt.clf()
        
        handles = []
        labels = []
        for i in xrange(len(self.particles)):
            t = self.t[i][self.start:self.start+self.length]
            x = self.x[i][self.start:self.start+self.length]
            y = self.y[i][self.start:self.start+self.length]
            z = self.z[i][self.start:self.start+self.length]
            R = np.hypot(x, y)
            plt.scatter(z, R, c=t, cmap=cmap.next())
            handles.append(mpatches.Patch(color=lmap.next()))
            labels.append(self.label(self.particles[i]))
            
        plt.legend(handles, labels, ncol=1, loc=4, framealpha=0.5)
#        plt.legend(ncol=1, loc=4, framealpha=0.5)
        plt.draw()
            
    def label(self, particle):
        if particle == 'e-':
            return '$e^-$'
        elif particle == 'de+':
            return '$De^+$'
        elif particle == 'tr+':
            return '$Tr^+$'
        elif particle == 'p-':
            return '$H^-$'