# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 20:36:29 2015

@author: leben
Console dialog to view simulator parameters and run simulation
"""

import os
import settings
from utility import formats

def promptSimulator():
    s = settings.Settings()
    app = settings.Simulator()
    mainPage = """
    === EDIT SIMULATION PARAMS ===
    Current parameters are:
    Particle code       : {particleCode}
    Particle mass       : {mass}
    Particle charge     : {charge}
    Initial position    : {x0} {y0} {z0} m
    Initial velocity    : {vx0} {vy0} {vz0} m/s
    Using kinetic energy for initial velocity? {useKinetic}
    Kinetic energy      : {kinetic} keV
    Field code          : {fieldCode}
    Field base strength : {fieldStrength} Tesla
    Field gradients     : {fieldGradient}
    Field length        : {fieldLength} m
    Field frequency     : {fieldFreq}
    Initial time        : {t0} s
    End time            : {tend} s
    Timestep            : {h} s
    
    Options:
    {BOLD}1{ENDC}   Select particle
    {BOLD}2{ENDC}   Set initial position
    {BOLD}3{ENDC}   Set initial velocity
    {BOLD}4{ENDC}   Select magnetic field profile
    {BOLD}5{ENDC}   Set initial time, end time and timestep
    {BOLD}q{ENDC}   Save and exit
    """[1:-1]
    
def promptParticleCode():
    mainPage = """
    === SELECT PARTICLE ===
    Current parameters are:
    Particle code   : {particleCode}
    Particle mass   : {mass}
    Particle charge : {charge}
    
    Particle options:
    {BOLD}1{ENDC} {ULINE}e{ENDC}-    {BOLD}3{ENDC} {ULINE}n{ENDC}     {BOLD}5{ENDC} {ULINE}T{ENDC}r+
    {BOLD}2{ENDC} {ULINE}p{ENDC}+    {BOLD}4{ENDC} {ULINE}D{ENDC}e+   {BOLD}6{ENDC} {ULINE}H{ENDC}e+
    
    {BOLD}7{ENDC} {ULINE}m{ENDC}anual
    """[1:-1]
    
    






























