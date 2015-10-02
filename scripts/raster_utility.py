# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 03:09:58 2015

@author: leben
For big data, since interactive plotting is too heavy
"""

import numpy as np
import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt

from plot_utility import extractData

def plotFront(fn, out, comment='#', skipline=1, skiprow=2):
    """Plot of y = f(x)
    """
    t, x, y = extractData(fn, [0, 1, 2])
    plt.scatter(x[skipline::skiprow], y[skipline::skiprow], c=t[skipline::skiprow],
             cmap='gray')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.savefig(out)
    
def plotTop(fn, out, comment='#', skipline=1, skiprow=2):
    """Plot of z = f(x)
    """
    t, x, z = extractData(fn, [0, 1, 3])
    plt.scatter(x[skipline::skiprow], z[skipline::skiprow], c=t[skipline::skiprow], cmap='gray_r')
    plt.xlabel('x (m)')
    plt.ylabel('z (m)')
    plt.savefig(out)
    
def plotRight(fn, out, comment='#', skipline=1, skiprow=2):
    """Plot of y = f(z)
    """
    t, y, z = extractData(fn, [0, 2, 3])
    plt.scatter(z[skipline::skiprow], y[skipline::skiprow], c=t[skipline::skiprow], cmap='gray_r')
    plt.xlabel('z (m)')
    plt.ylabel('y (m)')
    plt.savefig(out)

def plotPoloid(fn, out, comment='#', skipline=1, skiprow=2):
    """Plot of R = x**2 + y**2 vs z
    """
    t, x, y, z = extractData(fn, [0, 1, 2, 3])
    x = np.array(x)
    y = np.array(y)
    R = np.hypot(x, y)
    plt.scatter(R[skipline::skiprow], z[skipline::skiprow], c=t[skipline::skiprow], cmap='gray_r')
    plt.xlabel('R (m)')
    plt.ylabel('z (m)')
    plt.savefig(out)
    
if __name__ == '__main__':   
    import argparse as ap
    parser = ap.ArgumentParser(description='Utility script for plotting files')
    parser.add_argument('filename')
    parser.add_argument('output')
    parser.add_argument('--front', dest='front', action='store_true',
                        help='Do not plot front view')
    parser.add_argument('--top', dest='top', action='store_true',
                        help='Do not plot top view')
    parser.add_argument('--right', dest='right', action='store_true',
                        help='Do not plot right view')
    parser.add_argument('--no_poloid', dest='poloid', action='store_false',
                        help='Do not plot with poloidal coordinate system')
    parser.add_argument('--skiprow', dest='skiprow', default=1,
                        help='To reduce data point')
    
    args = parser.parse_args()
    
    if args.front:
        with open(args.filename, 'r') as f:
            plotFront(f, args.output, skiprow=args.skiprow)
    if args.top:
        with open(args.filename, 'r') as f:
            plotTop(f, args.output, skiprow=args.skiprow)
    if args.right:
        with open(args.filename, 'r') as f:
            plotRight(f, args.output, skiprow=args.skiprow)
    if args.poloid:
        with open(args.filename, 'r') as f:
            plotPoloid(f, args.output, skiprow=args.skiprow)