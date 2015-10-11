# Charged Particle Motion within Magnetic Field

[lebenasa@hotmail.com]:lebenasa@hotmail.com
Author: Leben Asa ([lebenasa@hotmail.com][])

This application simulates charged particle trajectory within magnetic field by
numerically solve Lorentz force equation. The simulation code was written in
C++ with heavy use of template metaprogramming. The simulation doesn't need any third party
library, but may not compile in older compiler with incomplete or partial C++11
support.

## Getting Started
We used __qmake__ for cross platform compiling. If your system already has Qt installed, you can call `qmake` from Terminal or Qt Command Prompt (Windows):
> `` $> qmake ``
>
> `` $> make ``

The application binary can be found in `bin` directory. This application use old style
`stdin` for data and parameter input. We provided some scripts to run the simulation in `script` directory. 
To run scripts:
> `` $> bash script_name.sh ``

*The provided scripts were bash scripts. Windows user may prefer PowerShell scripts instead.*

## Scripting with Python
We used Python to build elaborate setup on top of the simulation program.
The useful ones are *settings.py* and *magnetic.py*. 
*settings.py* contains helper class `Settings` which can save and load folder configuration,
such as output directory and output filename.
*magnetic.py* contains helper class `Application` which can save and load simulation configuration
and run the simulation itself.
Since the configurations are stored in JSON files, user can use both classes as if they were
singletons.

A simple example:
> `` import os ``
> `` from settings import Settings ``
> `` from magnetic import Application ``
>
> `` s = Settings() ``
> `` app = Application() ``
> `` s.outdir = os.path.join(s.rootdir, 'output') ``
> `` app.fieldCode = 'Tokamak' ``
> `` app.useKineticEnergy = True ``
> `` # Run simulation with several kinetic energy levels ``
> `` for E in range(1, 5, 0.5): ``
> ``     s.outfile = 'Tokamak_E{E}'.format(E=E) ``
> `` 	 s.save() ``
> ``	 app.kineticEnergy = E ``
> ``	 app.execute() ``

More sample and demonstration may (or may not) be added in future.