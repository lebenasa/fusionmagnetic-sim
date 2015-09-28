#!/bin/bash

SIMROOT=$HOME/Labs/magnetic/
LM=$SIMROOT/bin/magnetic
OUTDIR=$SIMROOT/output/

DATE=`date +%Y.%m.%d.%H.%M.%S`
CASE=HomogenField
OUTLST=$OUTDIR/$CASE-$DATE.dat

# mkdir $OUTDIR

grep -v '#' << END_INPUT | $LM #>& $OUTLST
de+             # Particle codename
0.0 0.0 0.0     # Initial position (m)
Y               # Y: Initial velocity in keV instead of m/s
15              # Plasma temperature (keV)
# n             # Another example
# 1.0 1.0 1.0   # Initial velocity (m/s)
Homogen         # Magnetic field codename
4.7 0.0 0.0     # Magnetic field strength (Tesla)
0.0             # Initial time (s)
1.0E-04         # End time (s)
1.0E-09         # Timestep (s)
END_INPUT
