#ifndef APPLICATION_H
#define APPLICATION_H

#include <istream>
#include <iostream>
#include <iomanip>
#include <string>
#include <regex>
#include <chrono>
#include <ctime>
#include <locale>
#include "simulator.h"

class Application
{
public:
    Application() = default;
    ~Application() = default;

    pl::Simulator prepareSimulator();
    void writeParticleData(const pl::Simulator& simulator);

    void bindSimulator(pl::Simulator &sim);
    void writeOutputHeader();
    void writeOutputFooter();

private:
    void prepareParticle(pl::Simulator& sim);
    void resumeSimulation(pl::Simulator& sim);
    void prepareMagneticField(pl::Simulator& sim);
    void prepareParameters(pl::Simulator& sim);

    std::chrono::time_point<std::chrono::system_clock> started;
};

#endif // APPLICATION_H
