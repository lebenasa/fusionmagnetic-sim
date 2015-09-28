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

#ifndef SIMULATORLIB_H
#define SIMULATORLIB_H

#include <ostream>
#include <memory>
#include <cmath>
#include <cassert>
#include <functional>
#include <type_traits>
#include <initializer_list>
#include <array>
#include <vector>

namespace pl 
{
    using dec = double;
    
    // Dimensional analysis utilities
    struct UnitType {    };
    
    template < int M, int L, int T, int K, int C, int N >
    struct Unit : UnitType
    {
        enum { m=M, l=L, t=T, k=K, c=C, n=N };
    };
    
    template < class T >
    constexpr bool Is_unit()
    {
        return std::is_base_of< UnitType, T >::value;
    }
    
    template < bool B, class T = void >
    using Enable_if = typename std::enable_if<B, T>::type;
    
    template < bool B, class T, class F >
    using Conditional = typename std::conditional<B, T, F>::type;
    
    using dimless   = Unit < 0, 0, 0, 0, 0, 0 >;
    using kilogram  = Unit < 1, 0, 0, 0, 0, 0 >;
    using meter     = Unit < 0, 1, 0, 0, 0, 0 >;
    using second    = Unit < 0, 0, 1, 0, 0, 0 >;
    using kelvin    = Unit < 0, 0, 0, 1, 0, 0 >;
    using coulomb   = Unit < 0, 0, 0, 0, 1, 0 >;
    using mol       = Unit < 0, 0, 0, 0, 0, 1 >;
    
    template < class T >
    constexpr bool Is_dimless()
    {
        return std::is_same< T, dimless >::value;
    }

    template < class T >
    constexpr Enable_if< Is_unit<T>(), bool > Is_even()
    {
        return (T::m % 2) + (T::l % 2) + (T::t % 2) +
                (T::k % 2) + (T::c % 2) + (T::n % 2) == 0;
    }
    
    template < class U1, class U2 >
    struct Uplus {
        using type = Unit < U1::m+U2::m, U1::l+U2::l, U1::t+U2::t,
        U1::k+U2::k, U1::c+U2::c, U1::n+U2::n >;
    };
    
    template < class U1, class U2 >
    using Unit_plus = typename Uplus<U1, U2>::type;
                                                   
    template < class U1, class U2 >
    struct Uminus {
        using type = Unit < U1::m-U2::m, U1::l-U2::l, U1::t-U2::t,
        U1::k-U2::k, U1::c-U2::c, U1::n-U2::n >;
    };
    
    template < class U1, class U2 >
    using Unit_minus = typename Uminus<U1, U2>::type;

    template < class U1, int pow >
    struct Umultiply {
        using type = Unit < U1::m * pow, U1::l * pow, U1::t * pow,
        U1::k * pow, U1::c * pow, U1::n * pow >;
    };

    template < class U1, int pow >
    using Unit_multiply = typename Umultiply<U1, pow>::type;

    template < class U >
    struct Uhalf
    {
        static_assert( Is_even<U>(), "Unit contains odd power" );
        using type = Unit < U::m / 2, U::l / 2, U::t / 2,
        U::k / 2, U::c / 2, U::n / 2 >;
    };

    template < class U >
    using Unit_half = typename Uhalf<U>::type;
    
    using mps       = Unit_minus< meter, second >;
    using mpss      = Unit_minus< mps, second >;
    using newton    = Unit_plus< kilogram, mpss >;
    using joule     = Unit_plus< newton, meter >;
    using watt      = Unit_minus< joule, second >;
    using ampere    = Unit_minus< coulomb, second >;
    using volt      = Unit< 1, 2, -2, 0, -1, 0 >;
    using ohm       = Unit_minus< volt, ampere >;
    using tesla     = Unit< 1, 0, -1, 0, -1, 0 >;
    
    template < class U >
    struct Quantity 
    {
        dec val;
        explicit constexpr Quantity() : val { 0.0 } 
        { 
            static_assert( Is_unit<U>(), "Quantity requires valid unit as parameter" );
        }
        explicit constexpr Quantity(dec d) : val{ d } 
        { 
            static_assert( Is_unit<U>(), "Quantity requires valid unit as parameter" );
        }

        Quantity(const Quantity& v) : val{ v.val }
        {
        }

        Quantity(Quantity&& v)
        {
            val = std::move(v.val);
        }

        Quantity& operator=(const Quantity& v)
        {
            val = v.val;
            return *this;
        }
        
        operator Conditional< Is_dimless<U>(), dec, void > () const
        {
            return val;
        }
        
        Quantity<U>& operator+=(const Quantity<U>& b)
        {
            val += b.val;
            return *this;
        }
        
        Quantity<U>& operator-=(const Quantity<U>& b)
        {
            val -= b.val;
            return *this;
        }
        
        Quantity<U>& operator*=(dec b)
        {
            val *= b;
            return *this;
        }
        
        Quantity<U>& operator/=(dec b)
        {
            val /= b;
            return *this;
        }
        
        Quantity<U>& operator-()
        {
            val = -val;
            return *this;
        }
    };
    
    template < class U >
    Conditional< Is_dimless<U>(), dec, Quantity<U> > make_quantity(dec v)
    {
        using ret_type = Conditional< Is_dimless<U>(), dec, Quantity<U> >;
        return ret_type{v};
    }

    template < class U, Enable_if< Is_dimless<U>(), dec > >
    dec dimless_cast(const Quantity<U>& v)
    {
        return v.val;
    }

    template < class U >
    Quantity<Unit_plus<U, dimless>> operator+(const Quantity<U>& a, const Quantity<U>& b) 
    {
        return Quantity<Unit_plus<U, dimless>>{ a.val + b.val };
    }
    
    template < class U >
    Quantity<Unit_plus<U, dimless>> operator-(const Quantity<U>& a, const Quantity<U>& b)
    {
        return Quantity<Unit_plus<U, dimless>>{ a.val - b.val };
    }
    
    template < class U1, class U2 >
    constexpr Quantity<Unit_plus<U1, U2>> operator*(const Quantity<U1>& a, const Quantity<U2>& b) 
    {
        return Quantity<Unit_plus<U1, U2>>{ a.val * b.val };
    }
    
    template < class U1, class U2 >
    constexpr Quantity<Unit_minus<U1, U2>> operator/(const Quantity<U1>& a, const Quantity<U2>& b)
    {
        return Quantity<Unit_minus<U1, U2>>{ a.val / b.val };
    }
    
    template < class U >
    constexpr Quantity<Unit_plus<U, dimless>> operator*(const Quantity<U>& a, dec b)
    {
        return Quantity<Unit_plus<U, dimless>>{ a.val * b };
    }
    
    template < class U >
    constexpr Quantity<Unit_plus<U, dimless>> operator*(dec b, const Quantity<U>& a)
    {
        return Quantity<Unit_plus<U, dimless>>{ a.val * b };
    }
     
    template < class U >
    constexpr Quantity<Unit_plus<U, dimless>> operator/(const Quantity<U>& a, dec b)
    {
        return Quantity<Unit_plus<U, dimless>>{ a.val / b };
    }
    
    template < class U >
    constexpr Quantity<Unit_minus<dimless, U>> operator/(dec b, const Quantity<U>& a)
    {
        return Quantity<Unit_minus<dimless, U>>{ b / a.val };
    }
    
    template < class U >
    bool operator==(const Quantity<U>& a, const Quantity<U>& b)
    {
        return a.val == b.val;
    }
    
    template < class U >
    bool operator!=(const Quantity<U>& a, const Quantity<U>& b)
    {
        return a.val != b.val;
    }
    
    template < class U >
    bool operator<=(const Quantity<U>& a, const Quantity<U>& b)
    {
        return a.val <= b.val;
    }
    
    template < class U >
    bool operator<(const Quantity<U>& a, const Quantity<U>& b)
    {
        return a.val < b.val;
    }
    
    template < class U >
    bool operator>=(const Quantity<U>& a, const Quantity<U>& b)
    {
        return a.val >= b.val;
    }
    
    template < class U >
    bool operator>(const Quantity<U>& a, const Quantity<U>& b)
    {
        return a.val > b.val;
    }
    
    template < class U >
    Quantity<Unit_plus<U, U>> square(const Quantity<U>& v)
    {
        return Quantity<Unit_plus<U, U>>{ v.val * v.val };
    }

    template < class U, int P >
    Quantity<Unit_multiply<U, P>> pow(const Quantity<U>& v)
    {
        return Quantity<Unit_multiply<U, P>>{ std::pow(v.val, P) };
    }

    inline Quantity<dimless> pow(const Quantity<dimless>& v, double power)
    {
        return Quantity<dimless>{ std::pow(v.val, power) };
    }

    template < class U >
    Quantity<Unit_half<U>> sqrt(const Quantity<U>& v)
    {
        return Quantity<Unit_half<U>>{ std::sqrt(v.val) };
    }

    template < class U >
    Quantity<U> hypot(const Quantity<U>& a, const Quantity<U>& b)
    {
        return Quantity<U>{ std::hypot(a.val, b.val) };
    }
    
    template < class U >
    Quantity<U> abs(const Quantity<U>& a)
    {
        return Quantity<U>{ std::abs(a.val) };
    }

    inline std::string suffix(int u, const char* x)
    {
        using namespace std;
        string suf;
        if (u) 
        {
            suf += x;
            if (1<u) suf += '0'+u;
            if (u<0)
            {
                suf += '-';
                suf += '0'-u;
            }
        }
        return suf;
    }
    
    template < class U >
    std::ostream& operator<<(std::ostream& os, Quantity<U> v)
    {
        return os << v.val << " " << suffix(U::m, "kg") << suffix(U::l, "m") <<
        suffix(U::t, "s") << suffix(U::k, "K") << suffix(U::c, "Coulomb") <<
        suffix(U::n, "mol");
    }
    
    // Mathematical Vector
    template < class U >
    class Vector
    {
        using unit = U;
        Quantity<U> x, y, z;
    public:
        Vector() = default;
        
        Vector(const Vector& v) : x{ v.x }, y{ v.y } , z{ v.z }
        {
        }

        Vector(Vector&& v)
        {
            x = std::move(v.x);
            y = std::move(v.y);
            z = std::move(v.z);
        }
        
        Vector(const Quantity<U>& v) : x{ v }, y{ v }, z{ v }
        { }
        
        Vector(const Quantity<U>& a, const Quantity<U>& b, const Quantity<U>& c)
            : x{ a }, y{ b }, z{ c }
        { }
        
        ~Vector()
        {
            static_assert( Is_unit<U>(), "Requires valid unit as parameter" );
        }
        
        Quantity<U> i() const { return x; }
        Quantity<U> j() const { return y; }
        Quantity<U> k() const { return z; }
        
        Vector<U>& operator=(const Vector<U>& v)
        {
            x = v.i(); y = v.j(); z = v.k();
            return *this;
        }
        
        Vector<U>& operator=(const Quantity<U>& v)
        {
            x = v; y = v; z = v;
            return *this;
        }
        
        Vector<U>& operator+=(const Quantity<U>& v)
        {
            x += v; y += v; z += v;
            return *this;
        }
        
        Vector<U>& operator+=(const Vector<U>& v) 
        {
            x += v.i(); y += v.j(); z += v.k();
            return *this;
        }
        
        Vector<U>& operator-=(const Quantity<U>& v)
        {
            x -= v; y -= v; z -= v;
            return *this;
        }
        
        Vector<U>& operator-=(const Vector<U>& v)
        {
            x -= v.i(); y -= v.j(); z -= v.k();
            return *this;
        }
        
        Vector<U>& operator*=(const dec& v)
        {
            x *= v; y *= v; z *= v;
            return *this;
        }
        
        Vector<U>& operator/=(const dec& v)
        {
            x /= v; y /= v; z /= v;
            return *this;
        }
        
        Vector<U> operator+(const Vector<U>& v)
        {
            return Vector<U>{ i() + v.i(), j() + v.j(), k() + v.k() };
        }
        
        Vector<U> operator-(const Vector<U>& v)
        {
            return Vector<U>{ i() - v.i(), j() - v.j(), k() - v.k() };
        }
    };

    template < class U >
    Vector<U> make_vector(dec v)
    {
        return Vector<U>{ make_quantity<U>(v) };
    }

    template < class U >
    Vector<U> make_vector(dec i, dec j, dec k)
    {
        return Vector<U>{ make_quantity<U>(i), make_quantity<U>(j), make_quantity<U>(k) };
    }

    template < class U >
    Vector<U> operator*(const Vector<U>& a, const dec& b)
    {
        return Vector<U>{ a.i() * b, a.j() * b, a.k() * b };
    }
    
    template < class U >
    Vector<U> operator*(const dec& a, const Vector<U>& b)
    {
        return Vector<U>{ a * b.i(), a * b.j(), a * b.k() };
    }
    
    template < class U1, class U2 >
    Vector<Unit_plus<U1, U2>> operator*(const Vector<U1>& a, const Quantity<U2>& b)
    {
        return Vector<Unit_plus<U1, U2>> { a.i() * b, a.j() * b, a.k() * b  };
    }
    
    template < class U1, class U2 >
    Vector<Unit_plus<U1, U2>> operator*(const Quantity<U1>& a, const Vector<U2>& b)
    {
        return Vector<Unit_plus<U1, U2>> { a * b.i(), a * b.j(), a * b.k() };
    }

    template < class U1, class U2 >
    Vector<Unit_plus<U1, U2>> operator*(const Vector<U1>& a, const Vector<U2>& b)
    {
        auto i = a.i() * b.i();
        auto j = a.j() * b.j();
        auto k = a.k() * b.k();
        return Vector<Unit_plus<U1, U2>>{ i, j, k };
    }

    template < class U >
    Vector<Unit_minus<dimless, U>> operator/(const dec& a, const Vector<U>& b)
    {
        return Vector<Unit_minus<dimless, U>> { a/b.i(), a/b.j(), a/b.k() };
    }
    
    template < class U >
    Vector<U> operator/(const Vector<U>& a, const dec& b)
    {
        return Vector<U> { a.i() / b, a.j() / b, a.k() / b };
    }
    
    template < class U1, class U2 >
    Vector<Unit_minus<U1, U2>> operator/(const Vector<U1>& a, const Quantity<U2>& b)
    {
        return Vector<Unit_minus<U1, U2>> { a.i() / b, a.j() / b, a.k() / b  };
    }
    
    template < class U1, class U2 >
    Vector<Unit_minus<U1, U2>> operator/(const Quantity<U1>& a, const Vector<U2>& b)
    {
        return Vector<Unit_minus<U1, U2>> { a / b.i(), a / b.j(), a / b.k() };
    }
    
    template < class U1, class U2 >
    Vector<Unit_minus<U1, U2>> operator/(const Vector<U1>& a, const Vector<U2>& b)
    {
        auto i = a.i() / b.i();
        auto j = a.j() / b.j();
        auto k = a.k() / b.k();
        return Vector<Unit_minus<U1, U2>>{ i, j, k };
    }

    template < class U >
    bool operator==(const Vector<U>& a, const Vector<U>& b)
    {
        return a.i() == b.i() && a.j() == b.j() && a.k() == b.k();
    }

    template < class U >
    bool operator !=(const Vector<U>& a, const Vector<U>& b)
    {
        return !(a == b);
    }

    template < class U1, class U2 >
    Vector<Unit_plus<U1, U2>> cross(const Vector<U1>& a, const Vector<U2>& b)
    {
        auto x = a.j()*b.k() - a.k()*b.j();
        auto y = a.k()*b.i() - a.i()*b.k();
        auto z = a.i()*b.j() - a.j()*b.i();
        return Vector<Unit_plus<U1, U2>> { x, y, z };
    }
    
    template < class U1, class U2 >
    Quantity<Unit_plus<U1, U2>> dot(const Vector<U1>& a, const Vector<U2>& b)
    {
        return a.i()*b.i() + a.j()*b.j() + a.k()*b.k();
    }

    template < class U >
    Quantity<U> magnitude(const Vector<U>& a)
    {
        return Quantity<U>{ sqrt(dot(a, a).val) };
    }

    template < class U >
    Vector<U> abs(const Vector<U>& a)
    {
        return Vector<U>{ abs(a.i()), abs(a.j()), abs(a.k()) };
    }
    
    namespace literals 
    {
        constexpr Quantity<kilogram> operator"" _kg(long double d) { return Quantity<kilogram>{ static_cast<dec>(d) }; }
        constexpr Quantity<meter>    operator"" _m(long double d) { return Quantity<meter>{ static_cast<dec>(d) }; }
        constexpr Quantity<second>   operator"" _s(long double d) { return Quantity<second>{ static_cast<dec>(d) }; }
        constexpr Quantity<kelvin>   operator"" _kelvin(long double d) { return Quantity<kelvin>{ static_cast<dec>(d) }; }
        constexpr Quantity<coulomb>  operator"" _coulomb(long double d) { return Quantity<coulomb>{ static_cast<dec>(d) }; }
        constexpr Quantity<mol>      operator"" _mol(long double d) { return Quantity<mol>{ static_cast<dec>(d) }; }
        constexpr Quantity<newton>   operator"" _newton(long double d) { return Quantity<newton>{ static_cast<dec>(d) }; }
        constexpr Quantity<joule>    operator"" _joule(long double d) { return Quantity<joule>{ static_cast<dec>(d) }; }
        constexpr Quantity<watt>     operator"" _watt(long double d) { return Quantity<watt>{ static_cast<dec>(d) }; }
        constexpr Quantity<ampere>   operator"" _ampere(long double d) { return Quantity<ampere>{ static_cast<dec>(d) }; }
        constexpr Quantity<volt>     operator"" _volt(long double d) { return Quantity<volt>{ static_cast<dec>(d) }; }
        constexpr Quantity<ohm>      operator"" _ohm(long double d) { return Quantity<ohm>{ static_cast<dec>(d) }; }
        constexpr Quantity<tesla>    operator"" _tesla(long double d) { return Quantity<tesla>{ static_cast<dec>(d) }; }
    }   // namespace literals
    
    // 4-th Order Runge-Kutta routine
    namespace odeint {
        template < class TY, class TX, class TR, class... Args >
        struct rk4
        {
            TY operator()(TX x, TY y, TX h, std::function< TR(TX, TY) > derive, Args... args)
            {
                auto k1 = derive(x, y);
                auto k2 = derive(x + 0.5*h, y + h * 0.5*k1);
                auto k3 = derive(x + 0.5*h, y + h * 0.5*k2);
                auto k4 = derive(x + h, y + h * k3);
                return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4);
            }
        };
    }   // namespace odeint
}   // namespace pl

#endif // SIMULATORLIB_H










