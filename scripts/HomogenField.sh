#!/bin/bash

SIMROOT=$HOME/Labs/magnetic/
LM=$SIMROOT/bin/magnetic
OUTDIR=$SIMROOT/output/

DATE=`date +%Y.%m.%d.%H.%M.%S`
CASE=HomogenField
OUTLST=$OUTDIR/$CASE-$DATE.dat

mkdir $OUTDIR

grep -v '#' << END_INPUT | $LM >& $OUTLST
# Job string, anything but Resume or Continue will start a fresh simulation
Simulate
# Initial particle position [x y z] (m)
0.0 0.0 0.0
# Plasma temperature (keV)
15
# Magnetic field string
Homogen
# Magnetic field strength [Bx By Bz] (Tesla)
0.0 0.0 4.7
# Timestep (second)
1.0E-13
# Sample skip, will write result after N times
10000
# Total iteration in this simulation session
1000000
END_INPUT


