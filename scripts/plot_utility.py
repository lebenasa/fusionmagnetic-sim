# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 06:46:33 2015

@author: leben
Helper function to plot files
"""

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
    
def tail(fn, cols=[0], comment='#'):
    """Extract last data (to continue simulation)
    """
    out = []
    for raw_line in fn:
        line = raw_line.strip('\n')
        if util.parsable(line, comment):
            out = line.split(' ')
    for i in range(len(out)):
        out[i] = float(out[i])
    return out[:len(cols)]
    
def plotFront(fn, comment='#', skipline=1, skiprow=2):
    """Plot of y = f(x)
    """
    t, x, y = extractData(fn, [0, 1, 2])
#    plt.scatter(x[skipline::skiprow], y[skipline::skiprow], c=t[skipline::skiprow],
#             cmap='gray_r')
    plt.plot(x[skipline::skiprow], y[skipline::skiprow], 'g', c=t[skipline::skiprow])
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.show()
    
def plotTop(fn, comment='#', skipline=1, skiprow=2):
    """Plot of z = f(x)
    """
    t, x, z = extractData(fn, [0, 1, 3])
#    plt.scatter(x[skipline::skiprow], z[skipline::skiprow], c=t[skipline::skiprow], cmap='gray_r')
    plt.plot(x[skipline::skiprow], z[skipline::skiprow], 'g', c=t[skipline::skiprow])
    plt.xlabel('x (m)')
    plt.ylabel('z (m)')
    plt.show()
    
def plotRight(fn, comment='#', skipline=1, skiprow=2):
    """Plot of y = f(z)
    """
    t, y, z = extractData(fn, [0, 2, 3])
#    plt.scatter(z[skipline::skiprow], y[skipline::skiprow], c=t[skipline::skiprow], cmap='gray_r')
    plt.plot(z[skipline::skiprow], y[skipline::skiprow], 'g', c=t[skipline::skiprow])
    plt.xlabel('z (m)')
    plt.ylabel('y (m)')
    plt.show()
    
def plotPoloid(fn, comment='#', skipline=1, skiprow=2):
    """Plot of R = x**2 + y**2 vs z
    """
    import numpy as np
    t, x, y, z = extractData(fn, [0, 1, 2, 3])
    x = np.array(x)
    y = np.array(y)
    R = np.hypot(x, y)
#    plt.scatter(R[skipline::skiprow], z[skipline::skiprow], c=t[skipline::skiprow], cmap='gray_r')
    plt.plot(R[skipline::skiprow], z[skipline::skiprow], 'g', c=t[skipline::skiprow])
    plt.xlabel('R (m)')
    plt.ylabel('z (m)')
    plt.show()
    
def plot3D(fn, comment='#', skipline=1, skiprow=2):
    from mpl_toolkits.mplot3d import Axes3D
    t, x, y, z = extractData(fn, [0, 1, 2, 3])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
#    ax.scatter(x, y, z, c=t, cmap='gray_r')
    plt.show()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    import argparse as ap
    parser = ap.ArgumentParser(description='Utility script for plotting files')
    parser.add_argument('filename')
    parser.add_argument('--front', dest='front', action='store_true',
                        help='Do not plot front view')
    parser.add_argument('--top', dest='top', action='store_true',
                        help='Do not plot top view')
    parser.add_argument('--right', dest='right', action='store_true',
                        help='Do not plot right view')
    parser.add_argument('--3d', dest='plot3d', action='store_true',
                        help='Plot 3d projection')
    parser.add_argument('--no_poloid', dest='poloid', action='store_false',
                        help='Do not plot with poloidal coordinate system')
    parser.add_argument('--skiprow', dest='skiprow', default=1,
                        help='To reduce data point')
    
    args = parser.parse_args()
    
    if args.front:
        with open(args.filename, 'r') as f:
            plotFront(f, skiprow=args.skiprow)
    if args.top:
        with open(args.filename, 'r') as f:
            plotTop(f, skiprow=args.skiprow)
    if args.right:
        with open(args.filename, 'r') as f:
            plotRight(f, skiprow=args.skiprow)
    if args.poloid:
        with open(args.filename, 'r') as f:
            plotPoloid(f, skiprow=args.skiprow)
    if args.plot3d:
        with open(args.filename, 'r') as f:
            plot3D(f)            
            
    