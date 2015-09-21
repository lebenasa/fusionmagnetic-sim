#include <thread>
#include <future>
#include "simulator.h"
using namespace std;
using namespace pl;

SimulatorData::SimulatorData()
    : m_temperature(15), h{ 1.0E-12 }
{
}

void SimulatorData::setTemperature(double keV)
{
    m_temperature = keV;
}

double SimulatorData::temperature() const
{
    return m_temperature;
}

Vector<mps> SimulatorData::initialVelocity(double mass_keV)
{
    return sqrt(2.0 * m_temperature / mass_keV) * light_speed;
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

void SimulatorData::setTimestep(Quantity<second> dt)
{
    h = dt;
}

Quantity<second> SimulatorData::timestep() const
{
    return h;
}

Simulator::Simulator()
    : SimulatorData{ }, deuterium{ "deuterium" },
      tritium{ "tritium" }, electron{ "electron" }, m_skip{ 1 }
{
    callback = [this](const Simulator& s) { s.deuteriumPosition(); };
}

void Simulator::setTemperature(double keV)
{
    SimulatorData::setTemperature(keV);
    auto phase = 90.0 / 180.0 * acos(-1);
    auto v_de = initialVelocity(deuterium_mass_keV);
    auto v_tr = initialVelocity(tritium_mass_keV);
    auto v_el = initialVelocity(electron_mass_keV);
    deuterium.setInitialVelocity(v_de.k(), phase, v_de.k());
    tritium.setInitialVelocity(v_tr.k(), phase, v_tr.k());
    electron.setInitialVelocity(v_el.k(), phase, v_el.k());
}

void Simulator::setInitialPosition(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z)
{
    SimulatorData::setInitialPosition(x, y, z);
    deuterium.setInitialPosition(initialPosition());
    tritium.setInitialPosition(initialPosition());
    electron.setInitialPosition(initialPosition());
}

void Simulator::setInitialPosition(const Vector<meter> &pos)
{
    SimulatorData::setInitialPosition(pos);
    deuterium.setInitialPosition(pos);
    tritium.setInitialPosition(pos);
    electron.setInitialPosition(pos);
}

void Simulator::setMagneticField(const std::function<Vector<tesla> (Vector<meter>)> & mag)
{
    deuterium.setMagneticField(mag);
    tritium.setMagneticField(mag);
    electron.setMagneticField(mag);
}

Vector<tesla> Simulator::magneticField(const Vector<meter> &pos)
{
    return deuterium.magneticField(pos);
}

Vector<tesla> Simulator::magneticField(Quantity<meter> x, Quantity<meter> y, Quantity<meter> z)
{
    return deuterium.magneticField(Vector<meter>{ x, y, z });
}

void Simulator::setSkip(size_t N)
{
    if (N > 0) m_skip = N;
}

size_t Simulator::skip() const
{
    return m_skip;
}

void Simulator::runUntil(Quantity<second> t)
{
    size_t N = (t / timestep()).val;
    runFor(N);
}

void Simulator::runSingleThreaded(size_t N)
{
    for (size_t i = 0; i < N; ++i)
    {
        deuterium.advance(timestep());
        tritium.advance(timestep());
        electron.advance(timestep());

        if (i % m_skip == 0)
        {
            callback(*this);
        }
    }
}

void Simulator::runMultiThreaded(size_t N)
{
    for (size_t i = 0; i < N / m_skip; ++i)
    {
        auto fut_de = async(launch::async, [this](){ for (size_t i = 0; i < m_skip; ++i) deuterium.advance(timestep()); });
        auto fut_tr = async(launch::async, [this](){ for (size_t i = 0; i < m_skip; ++i) tritium.advance(timestep()); });
        auto fut_el = async(launch::async, [this](){ for (size_t i = 0; i < m_skip; ++i) electron.advance(timestep()); });

        fut_de.get();
        fut_tr.get();
        fut_el.get();

        callback(*this);
        this_thread::sleep_for(chrono::milliseconds(1));
    }
}

void Simulator::runFor(size_t N)
{
    deuterium.initSimulation();
    tritium.initSimulation();
    electron.initSimulation();
    if (m_skip < 10000)
        runSingleThreaded(N);
    else
        runMultiThreaded(N);
}

void Simulator::reset()
{
    deuterium.initSimulation();
    tritium.initSimulation();
    electron.initSimulation();
}

Quantity<second> Simulator::time() const
{
    return deuterium.time();
}

Vector<mps> Simulator::deuteriumVelocity() const
{
    return deuterium.velocity();
}

Vector<mps> Simulator::tritiumVelocity() const
{
    return tritium.velocity();
}

Vector<mps> Simulator::electronVelocity() const
{
    return electron.velocity();
}

Vector<meter> Simulator::deuteriumPosition() const
{
    return deuterium.position();
}

Vector<meter> Simulator::tritiumPosition() const
{
    return tritium.position();
}

Vector<meter> Simulator::electronPosition() const
{
    return electron.position();
}

void Simulator::setDeuteriumVelocity(const Vector<mps> &vel)
{
    deuterium.setInitialVelocity(vel);
}

void Simulator::setTritiumVelocity(const Vector<mps> &vel)
{
    tritium.setInitialVelocity(vel);
}

void Simulator::setElectronVelocity(const Vector<mps> &vel)
{
    electron.setInitialVelocity(vel);
}

void Simulator::setDeuteriumPosition(const Vector<meter> &pos)
{
    deuterium.setInitialPosition(pos);
}

void Simulator::setTritiumPosition(const Vector<meter> &pos)
{
    tritium.setInitialPosition(pos);
}

void Simulator::setElectronPosition(const Vector<meter> &pos)
{
    electron.setInitialPosition(pos);
}

void Simulator::setCallback(const std::function< void(const Simulator &) > &cb)
{
    callback = cb;
}

















