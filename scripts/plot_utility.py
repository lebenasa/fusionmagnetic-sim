# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 06:46:33 2015

@author: leben
Helper function to plot files
"""

import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt

import utility as util

def extractData(fn, cols=[0], comment='#'):
    """Data extraction function
    callback must be a function object which will be called when the function
    read fn. callback function signature:
        def callback(data)
    where data is a list with size 8
    
    >>> extractData(['# comment', '10 10 10'])
    [[10.0]]
    >>> extractData(['# comment', '10 12 13'], [0, 1, 2])
    [[10.0], [12.0], [13.0]]
    """
    out = []
    for c in cols:
        out.append([])
    for raw_line in fn:
        line = raw_line.strip('\n')
        if util.parsable(line, comment):
            nums = line.split(' ')
            for i in range(len(out)):
                out[i].append(float(nums[cols[i]]))
    return out
    
def plotFront(fn, comment='#', skipline=1):
    """Plot of y = f(x)
    """
    t, x, y = extractData(fn, [0, 1, 2])
    plt.scatter(x[skipline:], y[skipline:], c=t[skipline:],
             cmap='gray')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.show()
    
def plotTop(fn, comment='#', skipline=1):
    """Plot of z = f(x)
    """
    t, x, z = extractData(fn, [0, 1, 3])
    plt.scatter(x[skipline:], z[skipline:], c=t[skipline:], cmap='gray_r')
    plt.xlabel('x (m)')
    plt.ylabel('z (m)')
    plt.show()
    
def plotRight(fn, comment='#', skipline=1):
    """Plot of y = f(z)
    """
    t, y, z = extractData(fn, [0, 2, 3])
    plt.scatter(z[skipline:], y[skipline:], c=t[skipline:], cmap='gray_r')
    plt.xlabel('z (m)')
    plt.ylabel('y (m)')
    plt.show()
    
def plotPoloid(fn, comment='#', skipline=1):
    """Plot of R = x**2 + y**2 vs z
    """
    import numpy as np
    t, x, y, z = extractData(fn, [0, 1, 2, 3])
    x = np.array(x)
    y = np.array(y)
    R = np.hypot(x, y)
    plt.scatter(R[skipline:], z[skipline:], c=t[skipline:], cmap='gray_r')
    plt.xlabel('R (m)')
    plt.ylabel('z (m)')
    plt.show()
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    import argparse as ap
    parser = ap.ArgumentParser(description='Utility script for plotting files')
    parser.add_argument('filename')
    parser.add_argument('--no_front', dest='front', action='store_false',
                        help='Do not plot front view')
    parser.add_argument('--no_top', dest='top', action='store_false',
                        help='Do not plot top view')
    parser.add_argument('--no_right', dest='right', action='store_false',
                        help='Do not plot right view')
    parser.add_argument('--no_poloid', dest='poloid', action='store_false',
                        help='Do not plot with poloidal coordinate system')
    
    args = parser.parse_args()
    
    if args.front:
        with open(args.filename, 'r') as f:
            plotFront(f)
    if args.top:
        with open(args.filename, 'r') as f:
            plotTop(f)
    if args.right:
        with open(args.filename, 'r') as f:
            plotRight(f)
    if args.poloid:
        with open(args.filename, 'r') as f:
            plotPoloid(f)
    