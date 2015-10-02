# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 03:35:49 2015

@author: Leben Asa

Set working directory, output file, simulation parameters etc.
The default value assumptions:
    magnetic/
        bin/
            magnetic (executable)
        doc/
        src/
        scripts/
            settings.py
            main.py, etc.
        out/
        tmp/
        README.md
        MAGNETIC.pro
"""

import os
import json

class Settings(object):
    """Settings class
    Stores and loads various directory used in application into JSON file
    """
    def __init__(self):
        if (os.path.exists("settings.json")):
            self.load()

    root = os.path.dirname(os.path.abspath('.'))# ..
    appname = os.path.join("bin", "magnetic")   # bin/magnetic
    app = os.path.join(root, appname)           # ../bin/magnetic
    outdir = os.path.join(root, "out")          # ../out
    outfile = "output"
    outext = ".csv"                             # ../out/output.csv
    appendDateToOutFile = True                  # ../out/output.DD.MM.YYYY.hh.mm.ss.csv
    tempdir = os.path.join(root, "tmp")         # ../tmp/

    def save(self):
        settings = {'root': self.root, 'app': self.app, 'outdir': self.outdir,
                    'outfile': self.outfile, 'outext': self.outext,
                    'appendDate': self.appendDateToOutFile,
                    'tempdir': self.tempdir}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    
    def load(self):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            self.root = settings['root']
            self.app = settings['app']
            self.outdir = settings['outdir']
            self.outfile = settings['outfile']
            self.outext = settings['outext']
            self.appendDateToOutFile = settings['appendDate']
            self.tempdir = settings['tempdir']
    
    def default(self):
        self.root = os.path.dirname(os.path.abspath('.'))
        self.app = os.path.join(self.root, "bin", "magnetic")
        self.outdir = os.path.join(self.root, "out")
        self.outfile = "output"
        self.outext = ".csv"
        self.appendDateToOutFile = True
        self.tempdir = os.path.join(self.root, "tmp")
        
    def outpath(self):
        return os.path.join(self.outdir, self.outfile) + self.outext

class Simulator(object):
    """Simulator class
    Stores and loads simulation parameters. Also has function to serialize
    parameters as input string
    """
    def __init__(self):
        if (os.path.exists("simulator.json")):
            self.load()
    
    params = {
    'particleCode': 'de+',
    'particleMass': 2.013553 * 1.660566E-27,
    'particleCharge': 1.6021892E-19,
    'x0': 0.0, 'y0': 0.0, 'z0': 0.0,
    'vx0': 1.0, 'vy0': 1.0, 'vz0': 1.0,
    'kinetic': 15, 'useKinetic': False,
    'fieldCode': 'Homogen',
    'fieldStrength': [0.0, 0.0, 4.7],
    'fieldGradient': [0.5, 0.5, 0.5],
    'fieldLength': 1.0,
    'fieldFreq': 0.5,
    'fieldParams1': 1.0,
    'fieldParams2': 1.0,
    't0': 0.0, 'tend': 1.0E-6, 'h': 1.0E-9
    }
    
    def save(self):
        with open('simulator.json', 'w') as f:
            json.dump(self.params, f)
    
    def load(self):
        with open('simulator.json', 'r') as f:
            p = json.load(f)
            self.params = p
    
    def default(self):
        self.particleCode = 'de+'
        self.particleMass = 2.013553 * 1.660566E-27
        self.particleCharge = 1.6021892E-19
        self.x0 = 0.0
        self.y0 = 0.0
        self.z0 = 0.0
        self.vx0 = 1.0
        self.vy0 = 1.0
        self.vz0 = 1.0
        self.kineticEnergy = 15
        self.useKineticEnergy = False
        self.fieldCode = 'Homogen'
        self.fieldBaseStrength = [0.0, 0.0, 4.7]
        self.fieldGradient = [0.5, 0.5, 0.5]
        self.fieldLength = 1.0
        self.fieldFreq = 0.5
        self.initialTime = 0.0
        self.endTime = 1.0E-6
        self.timeStep = 1.0E-9
        
    def serialize(self):
        """Serialize parameters as list of strings, ordered for simulation
        input purpose
        """
        p = []
        p.append(self.particleCode)
        if self.particleCode == 'manual':
            p.append(str(self.particleMass))
            p.append(str(self.particleCharge))
        p.append(str(self.x0))
        p.append(str(self.y0))
        p.append(str(self.z0))
        if self.useKineticEnergy:
            p.append('Y')
            p.append(str(self.kineticEnergy))
        else:
            p.append('n')
            p.append(str(self.vx0))
            p.append(str(self.vy0))
            p.append(str(self.vz0))
        p.append(self.fieldCode)
        if self.fieldCode == 'Drift':
            for val in self.fieldBaseStrength:
                p.append(str(val))
            p.append(str(self.fieldGradient[0]))
        elif self.fieldCode == 'Smooth':
            p.append(str(self.fieldBaseStrength[0]))
            p.append(str(self.fieldGradient[0]))
            p.append(str(self.fieldGradient[1]))
        elif self.fieldCode == 'Sharp':
            p.append(str(self.fieldBaseStrength[0]))
            p.append(str(self.fieldGradient[0]))
            p.append(str(self.fieldGradient[1]))
            p.append(str(self.fieldLength))
        elif self.fieldCode == 'Sine':
            p.append(str(self.fieldBaseStrength[0]))
            p.append(str(self.fieldGradient[0]))
            p.append(str(self.fieldGradient[1]))
            p.append(str(self.fieldLength))
            p.append(str(self.fieldFreq))
        elif self.fieldCode == 'Helix':
            p.append(str(self.fieldBaseStrength[0]))
            p.append(str(self.fieldBaseStrength[1]))
            for val in self.fieldGradient:
                p.append(str(val))
            p.append(str(self.fieldLength))
            p.append(str(self.fieldFreq))
        else:
            for val in self.fieldBaseStrength:
                p.append(str(val))
        p.append(str(self.initialTime))
        p.append(str(self.endTime))
        p.append(str(self.timeStep))
        return p
        
    @property
    def particleCode(self):
        """Particle code
        Recognizeable values are: e-, p+, n, de+, tr+, he+
        """
        return self.params['particleCode']
    
    @particleCode.setter
    def particleCode(self, code):
        available = ['manual', 'e-', 'p+', 'n', 'de+', 'tr+', 'he+', 'p-']
        for c in available:
            if code.lower() == c:
                self.params['particleCode'] = c
                break
            
    @property
    def particleMass(self):
        """Particle mass (kg)
        Used when using 'manual' particleCode
        """
        return self.params['particleMass']
        
    @particleMass.setter
    def particleMass(self, value):
        self.params['particleMass'] = value
        
    @property
    def particleCharge(self):
        """Particle charge (Coulomb)
        Used when using 'manual' particleCode
        """
        return self.params['particleCharge']
        
    @particleCharge.setter
    def particleCharge(self, value):
        self.params['particleCharge'] = value
    
    @property
    def x0(self):
        """Initial x position (m)"""
        return self.params['x0']
        
    @x0.setter
    def x0(self, value):
        self.params['x0'] = value

    @property
    def y0(self):
        """Initial y position (m)"""
        return self.params['y0']
        
    @y0.setter
    def y0(self, value):
        self.params['y0'] = value
        
    @property
    def z0(self):
        """Initial z position (m)"""
        return self.params['z0']
        
    @z0.setter
    def z0(self, value):
        self.params['z0'] = value

    @property
    def vx0(self):
        """Initial x velocity (m/s)"""
        return self.params['vx0']
        
    @vx0.setter
    def vx0(self, value):
        self.params['vx0'] = value

    @property
    def vy0(self):
        """Initial y velocity (m/s)"""
        return self.params['vy0']
        
    @vy0.setter
    def vy0(self, value):
        self.params['vy0'] = value
        
    @property
    def vz0(self):
        """Initial z velocity (m/s)"""
        return self.params['vz0']
        
    @vz0.setter
    def vz0(self, value):
        self.params['vz0'] = value

    @property
    def kineticEnergy(self):
        """Kinetic energy, if initial velocity weren't set manually (keV)"""
        return self.params['kinetic']
    
    @kineticEnergy.setter
    def kineticEnergy(self, value):
        self.params['kinetic'] = value
        
    @property
    def useKineticEnergy(self):
        """Use kinetic energy for initial velocity (bool)"""
        return self.params['useKinetic']
        
    @useKineticEnergy.setter
    def useKineticEnergy(self, value):
        self.params['useKinetic'] = value
    
    @property
    def fieldCode(self):
        """Magnetic field codename
        Recognizeable values: 'Homogen', 'Drift', 'Smooth', 'Sharp', 'Sine',
        'Helix'
        """
        return self.params['fieldCode']
    
    @fieldCode.setter
    def fieldCode(self, value):
        available = ['Homogen', 'Drift', 'Smooth', 'Sharp', 'Sine', 'Helix']
        for code in available:
            if (value == code):
                self.params['fieldCode'] = code
        
    @property
    def fieldBaseStrength(self):
        """Base strength value for magnetic field (Tesla)
        This property expect a list of 3 numbers. The number which eventually
        used depends on fieldCode:
        Homogen : [Bx0, By0, Bz0]
        Drift   : [Bx0, By0, Bz0]
        Smooth  : [B]
        Sharp   : [B]
        Sine    : [B]
        Helix   : [Bz0, Bteta0]
        """
        return self.params['fieldStrength']
        
    @fieldBaseStrength.setter
    def fieldBaseStrength(self, value):
        if len(value) == 0:
            return
        v = self.params['fieldStrength']
        if len(value) > 0:
            v[0] = value[0]
        if len(value) > 1:
            v[1] = value[1]
        if len(value) > 2:
            v[2] = value[2]
        self.params['fieldStrength'] = v
        
    @property
    def fieldGradient(self):
        """Field gradient value for magnetic field
        This property expect a list of 3 numbers. The number which eventually
        used depends on fieldCode:
        Homogen : []
        Drift   : [alpha]
        Smooth  : [alpha, beta]
        Sharp   : [alpha, beta]
        Sine    : [alpha, beta]
        Helix   : [alpha, beta, gamma]
        """
        return self.params['fieldGradient']
    
    @fieldGradient.setter
    def fieldGradient(self, value):
        if len(value) == 0:
            return
        v = self.params['fieldGradient']
        if len(value) > 0:
            v[0] = value[0]
        if len(value) > 1:
            v[1] = value[1]
        if len(value) > 2:
            v[2] = value[2]
        self.params['fieldGradient'] = v
        
    @property
    def fieldLength(self):
        """Field length parameter (m) for:
        Sharp Sine Helix
        """
        return self.params['fieldLength']
        
    @fieldLength.setter
    def fieldLength(self, value):
        self.params['fieldLength'] = value
        
    @property
    def fieldFreq(self):
        """Field frequency parameter for:
        Sine Helix
        """
        return self.params['fieldFreq']
        
    @fieldFreq.setter
    def fieldFreq(self, value):
        self.params['fieldFreq'] = value

    @property
    def initialTime(self):
        """Initial simulation time (s)"""
        return self.params['t0']
        
    @initialTime.setter
    def initialTime(self, value):
        self.params['t0'] = value
        
    @property
    def endTime(self):
        """End time of simulation (s), must be larger than initialTime"""
        return self.params['tend']
        
    @endTime.setter
    def endTime(self, value):
        if (value > self.initialTime):
            self.params['tend'] = value
        
    @property
    def timeStep(self):
        """Time step interval for ode-solver (s)"""
        return self.params['h']
    
    @timeStep.setter
    def timeStep(self, value):
        if (value > 0.0):
            self.params['h'] = value























