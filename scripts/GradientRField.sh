#!/bin/bash

SIMROOT=$HOME/Documents/DTESim/
LM=$SIMROOT/DTESim
OUTDIR=$SIMROOT/output/

DATE=`date +%Y.%m.%d.%H.%M.%S`
CASE=GradientRField
OUTLST=$OUTDIR/$CASE-$DATE.dat

grep -v '#' << END_INPUT | $LM >& $OUTLST
# Job string, anything but Resume or Continue will start a fresh simulation
Simulate
# Initial particle position [x y z] (m)
0.0 0.0 0.0
# Plasma temperature (keV)
15
# Magnetic field string
Drift
# Magnetic field strength Bz (Tesla)
4.7
# Magnetic field perpendicular gradient
0.5
# Timestep (second)
1.0E-13
# Sample skip, will write result after N times
10000
# Total iteration in this simulation session
10000000
END_INPUT



