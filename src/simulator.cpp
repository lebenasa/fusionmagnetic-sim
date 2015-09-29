#include <thread>
#include <future>
#include "simulator.h"
using namespace std;
using namespace pl;
using namespace pl::constants;
using namespace pl::literals;

Quantity<Unit_minus<keV, Unit_plus<mps, mps>>> toKeVLightSquare(Quantity<kilogram> mass)
{
    return (mass / atomic_mass) * 931501.0 / square(light_speed);
}

Quantity<keV> toKeV(Quantity<kelvin> temperature)
{
    return temperature * (1.0 / Quantity<kelvin>{ 1.1604505E07 });
}

Quantity<kilogram> toMass(Quantity<keV> e)
{
    auto cnst = 931501.0 * (square(1.0_m) / square(1.0_s));
    return (e * square(light_speed) / cnst) * atomic_mass;
}

Quantity<kelvin> toTemperature(Quantity<keV> e)
{
    return e * Quantity<kelvin>{ 1.1604505E07 };
}

// SimulatorData implementation
SimulatorData::SimulatorData()
    : h{ 1.0E-12 }, t0{ 0.0 }, tend{ 1.0 }
{
    bField = UniformField<tesla>{ };
}

void SimulatorData::setInitialPosition(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z)
{
    r = Vector<meter>{ x, y, z };
}

void SimulatorData::setInitialPosition(Vector<meter> pos)
{
    r = pos;
}

Vector<meter> SimulatorData::initialPosition() const
{
    return r;
}

void SimulatorData::setInitialVelocity(Quantity<mps> vx, Quantity<mps> vy, Quantity<mps> vz)
{
    v0 = Vector<mps>{ vx, vy, vz };
}

void SimulatorData::setInitialVelocity(Vector<mps> v)
{
    v0 = v;
}

void SimulatorData::setInitialVelocity(Quantity<keV> kinetic)
{
    using namespace pl::constants;
    v0 = Vector<mps>{ sqrt(2.0 * kinetic / toKeVLightSquare(m)) };
}

Vector<mps> SimulatorData::initialVelocity() const
{
    return v0;
}

void SimulatorData::setMagneticField(const MagneticField& field)
{
    bField = field;
}

Vector<tesla> SimulatorData::magneticField(const Vector<meter> &pos)
{
    return bField(pos);
}

Vector<tesla> SimulatorData::magneticField(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z)
{
    return bField(Vector<meter>{ x, y, z });
}

void SimulatorData::setTimestep(Quantity<second> dt)
{
    if (dt > 0.0_s)
        h = dt;
}

Quantity<second> SimulatorData::timestep() const
{
    return h;
}

void SimulatorData::setInitialTime(Quantity<second> time)
{
    if (t0 != time && time < endTime())
        t0 = time;
}

Quantity<second> SimulatorData::initialTime() const
{
    return t0;
}

void SimulatorData::setEndTime(Quantity<second> t)
{
    if (tend != t && t > initialTime())
        tend = t;
}

Quantity<second> SimulatorData::endTime() const
{
    return tend;
}

void SimulatorData::setParticleId(int id)
{
    using namespace pl::constants;
    pid = id;
    switch (id) {
    case 0:
        setMass(electron_mass);
        setCharge(electron_charge);
        break;
    case 1:
        setMass(neutron_mass);
        setCharge(neutron_charge);
        break;
    case 2:
        setMass(proton_mass);
        setCharge(proton_charge);
        break;
    case 3:
        setMass(deuterium_mass);
        setCharge(deuterium_charge);
        break;
    case 4:
        setMass(tritium_mass);
        setCharge(tritium_charge);
        break;
    case 5:
        setMass(alpha_mass);
        setCharge(alpha_charge);
        break;
    default:
        break;
    }
}

int SimulatorData::particleId() const
{
    return pid;
}

void SimulatorData::setMass(Quantity<kilogram> mass)
{
    m = mass;
    pid = -1;
}

Quantity<kilogram> SimulatorData::mass() const
{
    return m;
}

void SimulatorData::setCharge(Quantity<coulomb> charge)
{
    q = charge;
    pid = -1;
}

Quantity<coulomb> SimulatorData::charge() const
{
    return q;
}

// Monitor implementation
Monitor::Monitor()
    : stall{ chrono::milliseconds{0} }, buf_capacity{ 5000000 }
{
}

void Monitor::pushTime(const Quantity<second> &t)
{
    t_buf.emplace_back(t);
}

void Monitor::pushVelocity(const Vector<mps> &v)
{
    v_buf.emplace_back(v);
}

void Monitor::pushPosition(const Vector<meter> &r)
{
    r_buf.emplace_back(r);
}

Quantity<second> Monitor::pullTime()
{
    auto t = t_buf.front();
    t_buf.pop_front();
    return t;
}

Vector<mps> Monitor::pullVelocity()
{
    auto v = v_buf.front();
    v_buf.pop_front();
    return v;
}

Vector<meter> Monitor::pullPosition()
{
    auto r = r_buf.front();
    r_buf.pop_front();
    return r;
}

size_t Monitor::size() const
{
    return v_buf.size();
}

size_t Monitor::capacity() const
{
    return buf_capacity;
}

void Monitor::setCapacity(size_t sz)
{
    buf_capacity = sz;
}

bool Monitor::isEmpty()
{
    return size() == 0;
}

bool Monitor::isFull()
{
    return size() >= capacity();
}

chrono::milliseconds Monitor::stallTime() const
{
    return stall;
}

void Monitor::setStallTime(const chrono::milliseconds &t)
{
    stall = t;
}

void Monitor::callback()
{
    cb(*this);
}

void Monitor::setCallback(std::function<void (Monitor &)> fn)
{
    cb = fn;
}

// Simulator implementation
Simulator::Simulator()
    : SimulatorData{ }
{
    derive = [this](const Quantity<second>& tt, const Vector<mps>& vt)
    {
        utils::unused(tt);
        auto rt = r + (timestep() * vt);
        auto mg = magneticField(rt);
        return (charge() / mass()) * (cross(mg, vt));
    };
    monitor = make_shared<Monitor>(Monitor{});
}

Quantity<second> Simulator::time() const
{
    return t;
}

void Simulator::run()
{
    auto stall = chrono::milliseconds{ 10 };
    chrono::milliseconds total_stall{ 0 };
    auto pushData = [this]() {
        monitor->pushTime(t);
        monitor->pushPosition(r);
        monitor->pushVelocity(v);
    };
    auto stallSimulation = [&]() {
        while (!monitor->isEmpty())
        {
            this_thread::sleep_for(stall);
            total_stall += stall;
        }
    };

    v = initialVelocity();
    r = initialPosition();
    for (t = initialTime(); t < endTime(); t += timestep())
    {
        if (monitor->isFull())
            stallSimulation();
        monitor->setStallTime(total_stall);
        pushData();
        v = solver( t, v, timestep(), derive );
        r = r + v * timestep();
    }
    pushData();
}

shared_ptr<Monitor> Simulator::shareMonitor()
{
    return shared_ptr<Monitor>( monitor );
}

// SimulatorRK54 implementation
SimulatorRK54::SimulatorRK54()
    : SimulatorData{ }, monitor{ new Monitor }
{
    derive = [this](const X& x, const OdeSystem& y){
        auto rt = std::get<0>(y);
        auto vt = std::get<1>(y);
        rt += (t-x) * vt;
        auto mg = magneticField(rt);
        auto drdt = vt;
        auto dvdt = (charge() / mass()) * (cross(vt, mg));
        return ResSystem{ drdt, dvdt };
    };
}

SimulatorRK54::ResSystem SimulatorRK54::equations(const X &t, const OdeSystem &y)
{
    utils::unused(t);
    auto vt = std::get<1>(y);
    auto rt = r + (timestep() * vt);
    auto mg = magneticField(rt);
    auto drdt = vt;
    auto dvdt = (charge() / mass()) * (cross(vt, mg));
    return ResSystem{ drdt, dvdt };
}

Quantity<second> SimulatorRK54::time() const
{
    return t;
}

void SimulatorRK54::run()
{
    auto stall = chrono::milliseconds{ 10 };
    chrono::milliseconds total_stall{ 0 };
    auto pushData = [this]() {
        monitor->pushTime(t);
        monitor->pushPosition(r);
        monitor->pushVelocity(v);
    };
    auto stallSimulation = [&]() {
//        while (!monitor->isEmpty())
//        {
//            this_thread::sleep_for(stall);
//            total_stall += stall;
//        }
        monitor->callback();
    };

    v = initialVelocity();
    r = initialPosition();
    t = initialTime();
    for ( ; t < endTime(); )
    {
        if (monitor->isFull())
            stallSimulation();
        monitor->setStallTime(total_stall);
        pushData();

        auto y = OdeSystem{ r, v };
        auto odesys = solver( t, y, timestep(), derive, 1.0E-07 );
//        solver.calculateK(t, y, timestep(), derive);
//        auto odesys = solver.rk5(y);
        r = std::get<0>(odesys);
        v = std::get<1>(odesys);

        t += solver.stepUsed();
        if (t + solver.stepSuggested() > endTime())
            setTimestep(endTime() - t);
        else
            setTimestep(solver.stepSuggested());
//        t += timestep();
    }
    pushData();
    monitor->callback();
}

shared_ptr<Monitor> SimulatorRK54::shareMonitor()
{
    return shared_ptr<Monitor>{ monitor };
}
