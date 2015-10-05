# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 18:33:04 2015

@author: leben
Data acquisition and processing for magnetic field with radial gradiation
"""

import numpy as np
import settings
import magnetic as mag

from DriftSim import Drift

constants = {
'atomic_mass': 1.660566E-27,
'elementary_charge': 1.6021892E-19,
'light_speed': 2.9979E08
}

class ExperimentDrift(Drift):
    cdat = { }
    
    def __init__(self):
        super(ExperimentDrift, self).__init__()
        
    def execute(self, alphaStart, alphaEnd, alphaStep):
        alpha = alphaStart
        while alpha < alphaEnd:
            print 'Simulating with alpha = {alpha}'.format(alpha=alpha)
            self.simulate(alpha)
#            print 'Calculating difference with analytic solution. . .'
#            self.calculateDifference(alpha)
            print 'Calculating linear regression. . .'
            for particle in self.particles:
                self.calculateLinearRegression(particle, alpha)
#                self.calculateGuidingCenter(particle, alpha)
#            self.plotGuidingCenter(alpha)
#            self.plotLinearRegression(alpha)
            alpha += alphaStep
        
        print 'Calculating drift gradient. . .'
        self.calculateDeviations(alphaStart, alphaEnd, alphaStep)
#        print 'Plotting...'
#        for particle in self.particles:
#            self.plotDifferences(particle, alphaStart, alphaEnd, alphaStep)
        self.plotDeviations()
        
    def calculateLinearRegression(self, particle, alpha):
        from numpy import linalg
        import csv
        from plot_utility import extractData

        s = settings.Settings()        
        s.outfile = self.filename(particle, alpha)
        z = []
        t = []
        m = 0.0
        c = 0.0
        with open(s.outpath()) as f:
            t, x, y, z = extractData(f, [0, 1, 2, 3])
            R = np.hypot(np.array(x), np.array(y))
            A = np.vstack([t, np.ones(len(t))]).T
            m, c = linalg.lstsq(A, R)[0]
        
        s.outfile = self.filename(particle, alpha, 'drift_linreg_')
        with open(s.outpath(), 'w') as f:
            writer = csv.writer(f, delimiter=' ')
            for i in xrange(len(t)):
                writer.writerow([ t[i], m*t[i] + c, z[i] ])
        
    def calculateGuidingCenter(self, particle, alpha):
        from os import path
        import csv
        from plot_utility import extractData
        
        app = mag.Application()
        s = settings.Settings()
        
        gyro_period = self.gyro_period(app.fieldBaseStrength[2], self.charge(particle), self.mass(particle))
        center = []
        tp = []
        print gyro_period
        
        with open(path.join(s.outdir, self.filename(particle, alpha)) + s.outext) as f:
            t, x, y, z = extractData(f, [0, 1, 2, 3])
            R = np.hypot(x, y)
            period = 0
            Rs = []
            for i in xrange(len(t)):
                if period > gyro_period:
                    c = np.mean(Rs)
                    center.append(c)
                    Rs = []
                    if len(tp) == 0:
                        tp.append(period)
                    else:
                        tp.append(tp[-1] + period)
                    period = 0
                Rs.append(R[i])
                if i > 0:
                    period += t[i] - t[i-1]
                    
        with open(path.join(s.outdir, self.filename(particle, alpha, 'drift_center')) + s.outext, 'w') as f:
            writer = csv.writer(f, delimiter=' ')
            for i in xrange(len(center)):
                writer.writerow([ tp[i], center[i] ])
            
            
    def calculateDifference(self, alpha):
        from os import path
        import csv
        from plot_utility import extractData
        
        app = mag.Application()
        Bz0 = app.fieldBaseStrength[2]
        Ek = app.kineticEnergy
        
        s = settings.Settings()
        
        for particle in self.particles:
            xdiff = []
            ydiff = []
            zdiff = []
            tlist = []
            with open(path.join(s.outdir, self.filename(particle, alpha)) + s.outext) as f:
                tlist, x, y, z = extractData(f, [0, 1, 2, 3])
                self.prepareAnalytic(Ek, self.mass(particle))
                for i in xrange(len(tlist)):
                    xa, ya, za = self.analytic(tlist[i], Bz0, self.charge(particle), self.mass(particle))
                    xdiff.append(xa - x[i])
                    ydiff.append(ya - y[i])
                    zdiff.append(za - z[i])
            
            with open(path.join(s.outdir, self.filename(particle, alpha, 'drift_difference_')) + s.outext, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ')
                self.prepareAnalytic(Ek, self.mass(particle))
                for i in range(len(tlist)):
                    writer.writerow([ tlist[i], xdiff[i], ydiff[i], zdiff[i] ])
                    
    def calculateDeviations(self, alphaStart, alphaEnd, alphaStep):
        from os import path
        import csv
        from plot_utility import extractData

        s = settings.Settings()
                       
        for particle in self.particles:
            gradient = []
            alphas = []
            alpha = alphaStart
            while alpha < alphaEnd:
                s.outfile = self.filename(particle, alpha, 'drift_linreg_')
                with open(s.outpath()) as f:
                    t, R, z = extractData(f, [0, 1, 2])
                    g = (R[-1] - R[0]) / (t[-1] - t[0])
                    gradient.append(g)                    
                alphas.append(alpha)
                alpha += alphaStep
                
            with open(path.join(s.outdir, self.filename(particle, 0, 'drift_mean_')) + s.outext, 'w') as f:
                writer = csv.writer(f, delimiter=' ')
                for i in xrange(len(alphas)):
                    writer.writerow([ alphas[i], gradient[i] ])
                    
    def plotLinearRegression(self, alpha):
        import matplotlib.pyplot as plt
        from itertools import cycle
        from plot_utility import extractData
        
        s = settings.Settings()
        
        cols = cycle([ 'r', 'g', 'b' ])
        
        for particle in self.particles:
            s.outfile = self.filename(particle, alpha)
            c = cols.next()
            with open(s.outpath()) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                R = np.hypot(np.array(x), np.array(y))
                plt.plot(z, R, '.' + c, markersize=1, label=self.label(particle))
            s.outfile = self.filename(particle, alpha, 'drift_linreg_')
            with open(s.outpath()) as f:
                t, R, z = extractData(f, [0, 1, 2])
                plt.plot(z, R, '-' + c, linewidth=2)
        plt.legend()
        plt.tight_layout()
        plt.show()
                    
    def plotGuidingCenter(self, alpha):
        from os import path
        import matplotlib.pyplot as plt
        from plot_utility import extractData
        
        s = settings.Settings()
        
        for particle in self.particles:
            with open(path.join(s.outdir, self.filename(particle, alpha, 'drift_center')) + s.outext) as f:
                t, R = extractData(f, [0, 1])
                plt.plot(t, R, '--', label=self.label(particle))
                
        plt.show()
                    
    def plotDeviations(self):
        from os import path
        import matplotlib.pyplot as plt
        import itertools
        from plot_utility import extractData
        
        s = settings.Settings()
        symbols = itertools.cycle(['o', '^', 's'])
        
        for particle in self.particles:
            with open(path.join(s.outdir, self.filename(particle, 0, 'drift_mean_')) + s.outext, 'r') as f:
                alphas, means = extractData(f, [0, 1])
                plt.plot(alphas, means, symbols.next(), markersize=8, label=self.label(particle))
        
        plt.xlabel('$\\alpha$')
        plt.ylabel('$\\nabla B$ drift')
#        plt.legend(ncol=1, framealpha=0.5, loc=1)
        plt.tight_layout()
        plt.show()
        
    def plotDifferences(self, particle, alphaStart, alphaEnd, alphaStep):
        from os import path
        import matplotlib.pyplot as plt
        import itertools
        from plot_utility import extractData
        
        s = settings.Settings()
        symbols = itertools.cycle(['o', '^', 's'])
        
        alpha = alphaStart
        while alpha < alphaEnd:
            with open(path.join(s.outdir, self.filename(particle, alpha, 'drift_difference_')) + s.outext) as f:
                t, x, y, z = extractData(f, [0, 1, 2, 3])
                t = np.array(t)
                x = np.array(x)
                y = np.array(y)
                z = np.array(z)
                mag = self.magnitude(x, y, z)
                plt.plot(t, mag, '-', label='$\\alpha = {alpha:>02}'.format(alpha=alpha))
            alpha += alphaStep
        plt.xlabel('t')
        plt.ylabel('$\\nabla B$ drift')
        plt.legend(framealpha=0.5)
        plt.tight_layout()
        plt.show()
                    
    def magnitude(self, x, y, z):
        return np.sqrt(np.power(x, 2) + np.power(y, 2) + np.power(z, 2))

    def prepareAnalytic(self, kineticEnergy, mass):
        self.cdat['v0'] = [self.meterPerSecond(kineticEnergy, mass) for i in range(3)]
        self.cdat['phase'] = np.arctan(self.cdat['v0'][1] / self.cdat['v0'][0])
        self.cdat['vr'] = np.hypot(self.cdat['v0'][0], self.cdat['v0'][1])
        
    def analytic(self, t, Bz0, charge, mass):
        """Gives analytic position for charged particle in homogen field at
        a particular time
        """
        app = mag.Application()

        v0 = self.cdat['v0']
        phase = self.cdat['phase']
        vr = self.cdat['vr']
        gyro = self.gyro_freq(Bz0, charge, mass)
        rl = vr / gyro
        sign = np.sign(charge)

        xg = app.x0 + rl * np.sin(phase)
        yg = app.y0 - rl * np.cos(phase)
        xt = xg + rl * np.sin(gyro * t + (-1.0 * sign) * phase)
        yt = yg + sign * rl * np.cos(gyro * t + (-1.0 * sign) * phase)
        zt = app.z0 + v0[2] * t
        return [xt, yt, zt]
        
    def gyro_freq(self, Bz0, charge, mass):
        return abs(charge) * Bz0 / mass

    def gyro_period(self, Bz0, charge, mass):
        return 1.0 / self.gyro_freq(Bz0, charge, mass)
        
    def charge(self, particle):
        if particle == 'e-':
            return -1.0 * constants['elementary_charge']
        elif particle == 'de+':
            return constants['elementary_charge']
        elif particle == 'tr+':
            return constants['elementary_charge']
        elif particle == 'p-':
            return constants['elementary_charge']
            
    def mass(self, particle):
        if particle == 'e-':
            return 0.000549 * constants['atomic_mass']
        elif particle == 'de+':
            return 2.013553 * constants['atomic_mass']
        elif particle == 'tr+':
            return 3.015501 * constants['atomic_mass']
        elif particle == 'p-':
            return 1.0 * constants['atomic_mass']
            
    def meterPerSecond(self, keV, mass):
        return np.sqrt(2.0 * keV / self.toKeVLightSquare(mass))

    def toKeVLightSquare(self, mass):
        return (mass / constants['atomic_mass']) * 931501.0 /\
        constants['light_speed']**2
        
if __name__ == '__main__':  
    import argparse as ap
    parser = ap.ArgumentParser(description='Simulation for magnetic field with radial gradient')
    
    parser.add_argument('--alpha_start', default=0.1, type=float)
    parser.add_argument('--alpha_end', default=1.1, type=float)
    parser.add_argument('--alpha_step', default=0.1, type=float)
    
    args = parser.parse_args()
    app = ExperimentDrift()
    app.execute(args.alpha_start, args.alpha_end, args.alpha_step)