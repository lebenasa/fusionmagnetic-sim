/*
  Copyright (c) 2015, Leben Asa
  All rights reserved.
  
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
  * Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
  * Neither the name of the <organization> nor the
  names of its contributors may be used to endorse or promote products
  derived from this software without specific prior written permission.
  
  THIS SOFTWARE IS PROVIDED BY <copyright holder> ''AS IS'' AND ANY
  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#ifndef SIMULATION_H
#define SIMULATION_H

#include <map>
#include <type_traits>

#include "simulatorlib.hpp"

/*!
It's not quiet our application code but merely a specialization of existing lib,
so this file also goes under namespace "pl".
*/

namespace pl
{
using cpkg = Unit_minus<coulomb, kilogram>;
using vpm = Unit_minus<volt, meter>;
namespace constants
{
constexpr Quantity<kilogram>atomic_mass = Quantity<kilogram>{ 1.660566E-27 };
constexpr Quantity<coulomb> atomic_charge = Quantity<coulomb>{ 1.6021892E-19 };
constexpr Quantity<kilogram>electron_mass = 0.000549 * atomic_mass;
constexpr Quantity<coulomb> electron_charge = -1.0 * atomic_charge;
constexpr Quantity<kilogram>neutron_mass = 1.008665 * atomic_mass;
constexpr Quantity<coulomb> neutron_charge = 0.0 * atomic_charge;
constexpr Quantity<kilogram>proton_mass = 1.007276 * atomic_mass;
constexpr Quantity<coulomb> proton_charge = 1.0 * atomic_charge;
constexpr Quantity<kilogram>deuterium_mass = 2.013553 * atomic_mass;
constexpr Quantity<coulomb> deuterium_charge = 1.0 * atomic_charge;
constexpr Quantity<kilogram>tritium_mass = 3.015501 * atomic_mass;
constexpr Quantity<coulomb> tritium_charge = 1.0 * atomic_charge;
constexpr Quantity<kilogram>alpha_mass = 4.001503 * atomic_mass;
constexpr Quantity<coulomb> alpha_charge = 2.0 * atomic_charge;
constexpr Quantity<cpkg>    electron_qpm = electron_charge / electron_mass;
constexpr Quantity<cpkg>    neutron_qpm = neutron_charge / neutron_mass;
constexpr Quantity<cpkg>    proton_qpm = proton_charge / proton_mass;
constexpr Quantity<cpkg>    deuterium_qpm = deuterium_charge / deuterium_mass;
constexpr Quantity<cpkg>    tritium_qpm = tritium_charge / tritium_mass;
constexpr Quantity<cpkg>    alpha_qpm = alpha_charge / alpha_mass;
}   // namespace constants

namespace utils {
template < class T >
T unused(const T& t) { return t; }
}   // namespace utils

// Field value provider functors
template < class U >
class UniformField
{
    Vector<U> value;
public:
    UniformField() : value{ } { }
    UniformField(const Vector<U>& val) : value{ val } { }
    
    Vector<U> operator()(const Vector<meter>& position) const
    {
        utils::unused(position);
        return value;
    }
    
    void setValue(const Vector<U>& val)
    {
        value = val;
    }
};

// MotionSolver class
class MotionSolver
{
public:
    using rk4 = odeint::rk4< Vector<mps>, Quantity<second>, Vector<mpss> >;
    using ElectricField = std::function< Vector<vpm>(const Vector<meter>&) >;
    using MagneticField = std::function< Vector<tesla>(const Vector<meter>&) >;
    using VelPosPair = std::pair<Vector<mps>, Vector<meter>>;
    
    MotionSolver()
    {
        eField = UniformField<vpm>{};
        bField = UniformField<tesla>{};
        using namespace constants;
        qpm = electron_qpm;
        particle["electron"] = electron_qpm;
        particle["neutron"] = neutron_qpm;
        particle["proton"] = proton_qpm;
        particle["deuterium"] = deuterium_qpm;
        particle["tritium"] = tritium_qpm;
        particle["alpha"] = alpha_qpm;
    }
    virtual ~MotionSolver() { }
    
    MotionSolver(const std::string& particle_name)
    {
        eField = UniformField<vpm>{};
        bField = UniformField<tesla>{};
        using namespace constants;
        particle["electron"] = electron_qpm;
        particle["neutron"] = neutron_qpm;
        particle["proton"] = proton_qpm;
        particle["deuterium"] = deuterium_qpm;
        particle["tritium"] = tritium_qpm;
        particle["alpha"] = alpha_qpm;
        qpm = particle.at(particle_name);
        key = particle_name;
    }
    
    void setInitialVelocity(const Quantity<mps>& vxy, dec phase, const Quantity<mps> vz)
    {
        auto vx = vxy * std::sin(phase);
        auto vy = vxy * std::cos(phase);
        ivel = Vector<mps>{ vx, vy, vz };
    }
    void setInitialVelocity(const Vector<mps>& vel)
    {
        ivel = vel;
    }
    Vector<mps> initialVelocity() const
    {
        return ivel;
    }
    Vector<mps> velocity() const
    {
        return vel;
    }
    
    void setInitialPosition(const Vector<meter>& coordinate)
    {
        ipos = coordinate;
    }
    Vector<meter> initialPosition() const
    {
        return ipos;
    }
    Vector<meter> position() const
    {
        return pos;
    }
    
    void setParticle(const std::string& particle_name)
    {
        key = particle_name;
        qpm = particle.at(particle_name);
    }
    Quantity<cpkg> particle_prop() const
    {
        return qpm;
    }
    std::string particle_name() const
    {
        return key;
    }
    
    void setElectricField(const ElectricField& field)
    {
        eField = field;
    }
    Vector<vpm> electricField(const Vector<meter>& p)
    {
        return eField(p);
    }
    
    void setMagneticField(const MagneticField& field)
    {
        bField = field;
    }
    Vector<tesla> magneticField(const Vector<meter>& p)
    {
        return bField(p);
    }
    
    Quantity<second> time() const
    {
        return m_time;
    }
    Quantity<second> timestep() const { return m_h; }
    
    void initSimulation()
    {
        using namespace literals;
        m_time = 0.0_s;
        vel = ivel;
        pos = ipos;
    }
    
    virtual VelPosPair advance(const Quantity<second>& h)
    {
        using QT = Quantity<second>;
        using VMPS = Vector<mps>;
        m_h = h;
        vel = solve( m_time, vel, h, [this](const QT& t, const VMPS& v){ return derive(t, v); } );
        pos += vel * h;
        m_time += h;
        return VelPosPair{ vel, pos };
    }
    
protected:
    virtual Vector<mpss> derive(const Quantity<second>& t, const Vector<mps>& v)
    {
        utils::unused(t);
        auto p = pos + (m_h * v);
        auto el = eField(p);
        auto mg = bField(p);
        return qpm * (el + cross(mg, v));
    }
    
private:
    ElectricField eField;
    MagneticField bField;
    Vector<mps> ivel, vel;
    Vector<meter> ipos, pos;
    Quantity<second> m_time, m_h;
    Quantity<cpkg> qpm;
    std::map<std::string, Quantity<cpkg>> particle;
    std::string key;
    rk4 solve;
};
}   // namespace pl

#endif // SIMULATION_H














