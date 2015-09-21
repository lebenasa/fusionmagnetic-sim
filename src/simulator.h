#ifndef SIMULATOR_H
#define SIMULATOR_H

#include "simulation.hpp"
#include "fields.h"

namespace pl
{
constexpr double deuterium_mass_keV = 1875612;
constexpr double tritium_mass_keV   = 2808920.9;
constexpr double electron_mass_keV = 510.998;
constexpr Quantity<mps> light_speed = Quantity<mps>{ 2.9979E08 };

class SimulatorData
{
    double m_temperature;
    Vector<meter> r;
    Quantity<second> h;
public:
    SimulatorData();

    void setTemperature(double keV);
    double temperature() const;
    Vector<mps> initialVelocity(double mass_keV);

    void setInitialPosition(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z);
    void setInitialPosition(Vector<meter> pos);
    Vector<meter> initialPosition() const;

    void setTimestep(Quantity<second> h);
    Quantity<second> timestep() const;
};

class Simulator : public SimulatorData
{
    MotionSolver deuterium, tritium, electron;
    size_t m_skip;
    std::function< void(const Simulator&) > callback;
public:
    Simulator();

    void setTemperature(double keV);

    void setInitialPosition(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z);
    void setInitialPosition(const Vector<meter>& pos);

    // Facility to continue previous simulation
    void setDeuteriumVelocity(const Vector<mps>& vel);
    void setTritiumVelocity(const Vector<mps>& vel);
    void setElectronVelocity(const Vector<mps>& vel);
    void setDeuteriumPosition(const Vector<meter>& pos);
    void setTritiumPosition(const Vector<meter>& pos);
    void setElectronPosition(const Vector<meter>& pos);

    void setMagneticField(const std::function< Vector<tesla>(Vector<meter>) > &field);
    Vector<tesla> magneticField(const Vector<meter>& pos);
    Vector<tesla> magneticField(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z);

    void setSkip(size_t N);
    size_t skip() const;

    void runUntil(Quantity<second> t);
    void runFor(size_t N);
    void reset();

    Quantity<second> time() const;
    Vector<mps> deuteriumVelocity() const;
    Vector<mps> tritiumVelocity() const;
    Vector<mps> electronVelocity() const;
    Vector<meter> deuteriumPosition() const;
    Vector<meter> tritiumPosition() const;
    Vector<meter> electronPosition() const;

    void setCallback(const std::function< void(const Simulator&) >& callback);
private:
    void runSingleThreaded(size_t N);
    void runMultiThreaded(size_t N);
};
} // namespace pl

#endif // SIMULATOR_H
