# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 22:20:07 2015

@author: leben

A script to collect data that may show connection between timestep (h) with
error propagation.

FOR PERSONAL USE! USE AT OWN RISK!

Hypothesis:
    1   There is a timestep (h) value in which error doesn't grow (e.g. numeri-
        cally stable), this timestep is lower than gyro-period
    2   Error is a function of solely timestep*

* implies that magnetic field profile doesn't affect error

Goals:
    1   Find the upper limit of h in which numerical stability is observed
    2   Find out whether this upper limit of h works for all kind of magnetic
        field profile

Workflow:
OK  1   Simulate deuterium ion within homogen field using simulator
OK  2   Vary timestep as factor of gyro-frequency
OK  3   Simulate deuterium ion within homogen field using analytical solution
OK  4   Write difference in value of simulator result and analytical solution
        result, this is our error
OK  5   Plot error value as a function of time, the rate of error propagation
        is the gradient of this plot
OK  6   Answer Hypothesis 1, if the hipotesis is correct, determine the optimal
        timestep and continue
    7   Using optimal timestep, do simulations for every other magnetic field
        profile
    8   Using larger than the optimal timestep, do simulations for every other
        magnetic profile
    9   Verify Hypothesis 2
"""

import numpy as np
import os
import matplotlib as mpl
mpl.use('Qt4Agg')
import matplotlib.pyplot as plt

import settings
import magnetic as mag
import plot_utility as putil

constants = {
'atomic_mass': 1.660566E-27,
'elementary_charge': 1.6021892E-19,
'light_speed': 2.9979E08
}

class Experiment1:
    outfiles = []
    Bz0 = 4.7
#    mass = 2.013553 * constants['atomic_mass']
#    charge = 1.0 * constants['elementary_charge']
    mass = 1.0 * constants['atomic_mass']
    charge = -1.0 * constants['elementary_charge']
    step = 0.5
    count = 6
    cdat = { }

    def __init__(self):
        app = mag.Application()
        app.particleCode = 'p-'
        app.fieldCode = 'Homogen'
        app.x0 = 6.0
        app.y0 = 6.0
        app.z0 = 0.3
        app.useKineticEnergy = True
        app.kineticEnergy = 15
        app.fieldBaseStrength = [0.0, 0.0, self.Bz0]
        app.initialTime = 0.0
        app.endTime = 100  * self.gyro_period()
        app.save()
        self.gen_outfiles()

    def gyro_freq(self):
        return abs(self.charge) * self.Bz0 / self.mass

    def gyro_period(self):
        return 1.0 / self.gyro_freq()

    def gen_outfiles(self):
        self.outfiles = []

        for i in range(1, self.count):
            self.outfiles.append('Homogen_Protide_{ct:0>2}'.format(ct=i))

    def execute(self):
        import os
        print 'Running simulation'
        self.simulate()
        print 'Done. . .'
        print 'Running analytic solution'
        app = mag.Application()
        s = settings.Settings()
        self.prepAnalytic(app.kineticEnergy)
        anlfile = []
        simfile = []
        for i in range(1, self.count):
            infile = os.path.join(s.outdir, self.outfiles[i-1]) + s.outext
            outfile = os.path.join(s.outdir,
            'Analytic1_{ct:0>2}'.format(ct=i)) + s.outext
            self.calculateAnalytic(infile, outfile)
            errfile = os.path.join(s.outdir,
            'Error1_{ct:0>2}'.format(ct=i)) + s.outext
            self.calculateDifference(infile, outfile, errfile)
            simfile.append(infile)
            anlfile.append(outfile)
        print 'Done. . .'
        self.errorPlots()
        self.plotSuperimposed(simfile, anlfile[0])

    def simulate(self):
        app = mag.Application()
        s = settings.Settings()
        s.appendDateToOutFile = False
        s.save()

        for i in range(1, self.count):
            s.outfile = self.outfiles[i-1]
            s.save()
            app.timeStep = i * self.step * self.gyro_period()
            app.execute()

    def prepAnalytic(self, kineticEnergy):
        self.cdat['v0'] = [self.meterPerSecond(kineticEnergy) for i in range(3)]
        self.cdat['phase'] = np.arctan(self.cdat['v0'][1] / self.cdat['v0'][0])
        self.cdat['vr'] = np.hypot(self.cdat['v0'][0], self.cdat['v0'][1])

    def analytic(self, t):
        """Gives analytic position for charged particle in homogen field at
        a particular time
        """
        app = mag.Application()

        v0 = self.cdat['v0']
        phase = self.cdat['phase']
        vr = self.cdat['vr']
        rl = vr / self.gyro_freq()
        sign = np.sign(self.charge)

        xg = app.x0 - rl * np.sin(phase)
        yg = app.y0 + rl * np.cos(phase)
        xt = xg + rl * np.sin(self.gyro_freq() * t + (-1.0 * sign) * phase)
        yt = yg + sign * rl * np.cos(self.gyro_freq() * t + (-1.0 * sign) * phase)
        zt = app.z0 + v0[2] * t
        return [xt, yt, zt]

    def calculateAnalytic(self, fin, fout):
        """Calculate analytic solution for given simulation result file fin
        """
        import csv
        tlist = None
        with open(fin) as f:
            tlist = putil.extractData(f)[0]
        with open(fout, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ')
            for t in tlist:
                x, y, z = self.analytic(t)
                writer.writerow([t, x, y, z])

    def calculateDifference(self, fsim, fanl, fout):
        import csv
        xsim, ysim, zsim = [None, None, None]
        xanl, yanl, zanl = [None, None, None]
        tlist = None

        with open(fsim) as f:
            xsim, ysim, zsim = putil.extractData(f, [1, 2, 3])
            xsim = np.array(xsim)
            ysim = np.array(ysim)
            zsim = np.array(zsim)
        with open(fsim) as f:
            tlist = putil.extractData(f)[0]
        with open(fanl) as f:
            xanl, yanl, zanl = putil.extractData(f, [1, 2, 3])
            xanl = np.array(xanl)
            yanl = np.array(yanl)
            zanl = np.array(zanl)

        rsim = np.hypot(xsim, ysim)
        ranl = np.hypot(xanl, yanl)
        rerr = np.abs(ranl - rsim) / ranl# / len(ranl)
        zerr = np.abs(zanl - zsim) / zanl  # / len(zanl)
        rerr = np.cumsum(rerr)
        zerr = np.cumsum(zerr)

        with open(fout, 'w') as f:
            writer = csv.writer(f, delimiter=' ')
            for i in xrange(len(tlist)):
                writer.writerow([tlist[i], rerr[i], zerr[i]])

    def errorPlots(self):
        """Plot errors to answer hypothesis
        """
        s = settings.Settings()
        for i in range(1, self.count):
            errfile = os.path.join(s.outdir,
            'Error1_{ct:0>2}'.format(ct=i)) + s.outext
            with open(errfile) as f:
                t, r, z = putil.extractData(f, [0, 1, 2])
                r = np.array(r)
                z = np.array(z)
                t = np.array(t) * 10**6
                plt.plot(t, r, '--', label='{step} $\\tau_c$'.format(step=i*self.step))
        plt.xlabel('Time ($\\mu$s)')
        plt.ylabel('Error Accumulation')
        plt.legend(loc=2, ncol=2, framealpha=0.5)
        plt.tight_layout()
        plt.show()

    def plotSuperimposed(self, fsims, fanl):
        for i in range(len(fsims)):
            with open(fsims[i]) as f:
                t, x, y, z = putil.extractData(f, [0, 1, 2, 3])
                x = np.array(x)
                y = np.array(y)
#                r = np.hypot(x, y)
                plt.plot(z, y, 'o', label='{step} $\\tau_c$'.format(step=(i+1)*self.step))

        with open(fanl) as f:
            t, x, y, z = putil.extractData(f, [0, 1, 2, 3])
            x = np.array(x)
            y = np.array(y)
#            r = np.hypot(x, y)
            plt.plot(z, y, 'k-', linewidth=1.5, label='Analytic')

        plt.xlabel('z (m)')
        plt.ylabel('y (m)')
        plt.legend(ncol=self.count / 3, loc=4, framealpha=0.5)
        plt.tight_layout()
        plt.show()

    def meterPerSecond(self, keV):
        return np.sqrt(2.0 * keV / self.toKeVLightSquare(self.mass))

    def toKeVLightSquare(self, mass):
        return (self.mass / constants['atomic_mass']) * 931501.0 /\
        constants['light_speed']**2


if __name__ == '__main__':
    app = Experiment1()
    app.execute()
