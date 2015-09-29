# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 04:31:36 2015

@author: leben

Continuing simulation by probing file last data.
"""

import argparse as ap
import settings
import magnetic as mag
import utility as util
import plot_utility as putil

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Continue simulation')
    parser.add_argument('lastfile')
    parser.add_argument('newfile')
    parser.add_argument('endtime')
    
    # Using our JSON mechanism, we should be able to continue by changing
    # initial condition
    
    args = parser.parse_args()
    print args.lastfile
    print args.newfile
    print args.endtime

    if args.newfile == args.lastfile:
        print 'Unable to overwrite {fn}'.format(fn=args.lastfile)
        exit()
        
    t = 0.0
    x = 0.0
    y = 0.0
    z = 0.0
    vx= 0.0
    vy= 0.0
    vz= 0.0
    with open(args.lastfile) as f:
        t, x, y, z, vx, vy, vz = putil.tail(f, [0, 1, 2, 3, 4, 5, 6])
    
    app = mag.Application()
    app.x0 = x
    app.y0 = y
    app.z0 = z
    app.useKineticEnergy = False
    app.vx0 = vx
    app.vy0 = vy
    app.vz0 = vz
    app.initialTime = t
    app.endTime = args.endtime
    
    s = settings.Settings()
    s.outfile = args.newfile
    s.save()
    
    app.execute()
    
    success = False
    with open(s.outpath(), 'r') as out:
        for line in out:
            pass
        success = line.find("END OUTPUT") != -1
    print success