#ifndef SIMULATOR_H
#define SIMULATOR_H

#include "precompiled.h"
#include "fields.h"
#include "rk54.h"

namespace pl
{
constexpr double deuterium_mass_keV = 1875612;
constexpr double tritium_mass_keV   = 2808920.9;
constexpr double electron_mass_keV = 510.998;

class Monitor;
class SimulatorData
{
    using MagneticField = std::function< Vector<tesla>(const Vector<meter>&) >;

    Vector<meter> r;
    Vector<mps> v0;
    MagneticField bField;
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

    void setMagneticField(const MagneticField& field);
    Vector<tesla> magneticField(const Vector<meter>& pos);
    Vector<tesla> magneticField(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z);

    void setTimestep(Quantity<second> h);
    Quantity<second> timestep() const;

    void setInitialTime(Quantity<second> t);
    Quantity<second> initialTime() const;

    void setEndTime(Quantity<second> t);
    Quantity<second> endTime() const;

    virtual Quantity<second> time() const = 0;

    void setParticleId(int id);
    int particleId() const;

    void setMass(Quantity<kilogram> mass);
    Quantity<kilogram> mass() const;

    void setCharge(Quantity<coulomb> charge);
    Quantity<coulomb> charge() const;

    virtual void run() = 0;
    virtual std::shared_ptr<Monitor> shareMonitor() = 0;
};

class Simulator;
class SimulatorRK54;
class Monitor
{
    friend class SimulatorData;
    friend class Simulator;
    friend class SimulatorRK54;
    std::chrono::milliseconds stall;
    size_t buf_capacity, t_count, v_count, r_count;
    std::deque<Quantity<second>> t_buf;
    std::deque<Vector<mps>> v_buf;
    std::deque<Vector<meter>> r_buf;
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
    using dvdt = std::function< Vector<mpss>(const Quantity<second>& t, const Vector<mps>& v) >;
    using VelPosPair = std::pair<Vector<mps>, Vector<meter>>;

    RK4 solver;
    dvdt derive;
    Quantity<second> t;
    Vector<meter> r;
    Vector<mps> v;

    std::shared_ptr<Monitor> monitor;
public:
    Simulator();

    Quantity<second> time() const;

    void run();

    std::shared_ptr<Monitor> shareMonitor();
};

class SimulatorRK54 : public SimulatorData
{
    using X = Quantity<second>;
    using Y = Vector<meter>;
    using Dy = Vector<mps>;
    using D2y = Vector<mpss>;
    using OdeSystem = std::tuple< Y, Dy >;
    using ResSystem = std::tuple< Dy, D2y >;
    using Derivs = std::function< ResSystem(const X&, const OdeSystem&) >;

    odeint::RK54 solver;
    Derivs derive;
    X t;
    Y r;
    Dy v;

    std::shared_ptr<Monitor> monitor;
public:
    SimulatorRK54();

    Quantity<second> time() const;

    void run();

    std::shared_ptr<Monitor> shareMonitor();

protected:
    virtual ResSystem equations(const X& t, const OdeSystem& y);

private:
};

} // namespace pl

#endif // SIMULATOR_H
