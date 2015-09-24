#ifndef SIMULATOR_H
#define SIMULATOR_H

#include "precompiled.h"
#include "fields.h"

namespace pl
{
constexpr double deuterium_mass_keV = 1875612;
constexpr double tritium_mass_keV   = 2808920.9;
constexpr double electron_mass_keV = 510.998;

class SimulatorData
{
    Vector<meter> r;
    Vector<mps> v0;
    Quantity<second> h, t0, tend;
    Quantity<kilogram> m;
    Quantity<coulomb> q;
    int pid;
public:
    SimulatorData();

    void setInitialPosition(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z);
    void setInitialPosition(Vector<meter> pos);
    Vector<meter> initialPosition() const;

    void setInitialVelocity(Quantity<mps> vx, Quantity<mps> vy, Quantity<mps> vz);
    void setInitialVelocity(Vector<mps> v);
    void setInitialVelocity(Quantity<keV> kinetic);
    Vector<mps> initialVelocity() const;

    void setTimestep(Quantity<second> h);
    Quantity<second> timestep() const;

    void setInitialTime(Quantity<second> t);
    Quantity<second> initialTime() const;

    void setEndTime(Quantity<second> t);
    Quantity<second> endTime() const;

    void setParticleId(int id);
    int particleId() const;

    void setMass(Quantity<kilogram> mass);
    Quantity<kilogram> mass() const;

    void setCharge(Quantity<coulomb> charge);
    Quantity<coulomb> charge() const;
};

class Simulator;
class Monitor
{
    friend class Simulator;
    std::deque<Quantity<second>> t_buf;
    std::deque<Vector<mps>> v_buf;
    std::deque<Vector<meter>> r_buf;
    std::chrono::milliseconds stall;
    size_t buf_capacity;
public:
    Monitor();

    void pushTime(const Quantity<second>& t);
    void pushVelocity(const Vector<mps>& v);
    void pushPosition(const Vector<meter>& r);

    Quantity<second> pullTime();
    Vector<mps> pullVelocity();
    Vector<meter> pullPosition();

    size_t size() const;
    size_t capacity() const;
    void setCapacity(size_t sz);

    bool isEmpty();
    bool isFull();
    std::chrono::milliseconds stallTime() const;

protected:
    void setStallTime(const std::chrono::milliseconds& t);
};

class Simulator : public SimulatorData
{
    using RK4 = odeint::rk4< Vector<mps>, Quantity<second>, Vector<mpss> >;
    using Derive = std::function< Vector<mpss>(const Quantity<second>& t, const Vector<mps>& v) >;
    using MagneticField = std::function< Vector<tesla>(const Vector<meter>&) >;
    using VelPosPair = std::pair<Vector<mps>, Vector<meter>>;

    RK4 solver;
    Derive derive;
    MagneticField bField;
    Quantity<second> t;
    Vector<meter> r;
    Vector<mps> v;

    std::shared_ptr<Monitor> monitor;
public:
    Simulator();

    Quantity<second> time() const;

    void setMagneticField(const MagneticField& field);
    Vector<tesla> magneticField(const Vector<meter>& pos);
    Vector<tesla> magneticField(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z);

    void run();

    std::shared_ptr<Monitor> shareMonitor();
};

} // namespace pl

#endif // SIMULATOR_H
