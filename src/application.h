#ifndef APPLICATION_H
#define APPLICATION_H

#include "precompiled.h"
#include "simulator.h"

class Application
{
    pl::Simulator sim;
    std::shared_ptr<pl::Monitor> monitor;
public:
    Application();

    void exec();

private:
    void promptParticleData();
    void promptInitialCondition();
    void promptSimulationParams();
    void promptMagneticField();

    void writeOutputHeader();
    void writeOutputFooter();

    void writeOutput();

    bool isRunning;
    std::chrono::time_point<std::chrono::system_clock> started;
};

#endif // APPLICATION_H
