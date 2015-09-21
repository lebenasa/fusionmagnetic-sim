# Charged Particle Motion within Magnetic Field

[lebenasa@hotmail.com]:lebenasa@hotmail.com
Author: Leben Asa ([lebenasa@hotmail.com][])

This application simulates charged particle trajectory within magnetic field by
numerically solve Lorentz force equation. The simulation code was written in
C++ with heavy use of template metaprogramming. It doesn't need third party
library, but may not compile in older compiler with incomplete or partial C++11
support.

## Getting Started
We used __qmake__ for cross platform compiling. If your system already has Qt installed, you can call `qmake` from Terminal or Qt Command Prompt (Windows):
> `` $> qmake ``
>
> `` $> make ``

The application can be found in `bin` directory. This application use old style
`stdin` for data and parameter input. We provided some scripts in `script` directory. You can edit those scripts to change parameters and options. To run those scripts:
> `` $> bash script_name.sh ``

*The provided scripts were bash script. Windows user need to do minor
modification to run them with PowerShell*
