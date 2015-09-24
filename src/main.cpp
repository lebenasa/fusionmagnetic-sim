/*!
Charged Particle Motion Simulation in Pure C++

This project is a demonstration of how simulation can be written with no
dependancy except C++ Standard Library.

USAGE:
Please refer to Application.h for usage.

EXTENSION:
New fields should fulfill Callable concept, e.g. in form that can be accepted
by std::function, and should take vector of position as input and vector of
magnetic field strength as output.
To use different numerical method, simply replace the rk4 typename in
MotionSolver at file simulation.hpp.
*/

#include "application.h"

int main(int argc, char* argv[])
{
    pl::utils::unused(argc);
    pl::utils::unused(argv);
    Application app;
    app.exec();
    return 0;
}

