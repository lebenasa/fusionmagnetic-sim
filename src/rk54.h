#ifndef RK54_H
#define RK54_H

#include "simulatorlib.hpp"
#include <array>
#include <functional>
#include <vector>
#include <exception>
#include <type_traits>
#include <tuple>

/*! class rk54
 * Runge-Kutta Fehlberg implementation
 *
 * A very specialized ODE solver, made solely for this simulation project.
 * This class is rather hard to generalize. The ODE system contains quantity
 * with different dimensions, thus different types. Although the pattern is
 * rather clear, we decided to postpone parameterizing this class for another
 * chance.
 *
 * A huge comments at the bottom of the page showed our efforts, including
 * utilizing various metaprogramming technique to automatically create an
 * alias of std::tuple which holds correct dimensions of ODE system.
 * The big hurdle here is to broadcast values of various dimensions to the
 * tuple, in order to keep the core algorithm (e.g. the Runge Kutta
 * equation) organic (e.g. easy to read, maintain, explain). The specialized
 * implementation here remedied the problem temporarily by implementing
 * minimum operator overloads.
 *
 * At the hindsight, we feel that this class does too much things. Perhaps
 * the ODE system can be separated altogether?
 */

class rk54
{
public:
    using X = pl::Quantity<pl::second>;
    using Y = pl::Vector<pl::meter>;
    using Dy = pl::Vector<pl::mps>;
    using D2y = pl::Vector<pl::mpss>;
    using OdeSystem = std::tuple< Y, Dy >;
    using ResSystem = std::tuple< Dy, D2y >;
    using Derivs = std::function< ResSystem(X, OdeSystem) >;

    rk54()
    {
        a = { 0.0, 0.0, 0.2, 0.3, 3.0/5.0, 1, 7.0/8.0 };
        c = { 0.0, 37.0/378, 0, 250.0/621, 125.0/594, 0, 512.0/1771};
        d = { 0.0, 2825.0/27648, 0, 18575.0/48384, 13525.0/55296, 277.0/14336, 0.25 };
        b2 = { 0.0, 0.2 };
        b3 = { 0.0, 3.0/40, 9.0/40 };
        b4 = { 0.0, 0.3, -0.9, 1.2 };
        b5 = { 0.0, -11.0/54, 2.5, -70.0/27, 35.0/27 };
        b6 = { 0.0, 1631.0/55296, 175.0/512, 575.0/13824, 44275.0/110592, 253.0/4096 };
    }

    OdeSystem operator()(X x, OdeSystem y, X htry, Derivs derive,
                      pl::dec tolerance=1.0E-06)
    {
        /*! Runge Kutta Fehlberg routine based of Numerical Recipes in C
         *  Error criteria here is using "trick" from same book.
          */
        eps = tolerance;
        X h = htry;
        auto errMax = 0.0;
        OdeSystem y5;

        while (errMax <= 1.0)
        {
            calculateK(x, y, h, derive);
            auto y4 = flatify(rk4(y));
            y5 = flatify(rk5(y));
            auto err = y5 - y4;
            auto crit = std::abs(flatify(y)) + std::abs(flatify(h * y));
            auto errRatio = std::abs(crit / err);
            errMax = errRatio.max();
            errMax /= eps;

            auto htemp = shrink(h, errMax);
            h = (h >= X{ 0.0 }) ? std::max(htemp, 0.1 * h) : std::min(htemp, 0.1 * h);
            if (x+h - x < X{ 1.0E-30 })
                throw std::underflow_error("Underflow error, stepsize too small");
        }

        hdid = h;
        if (errMax < growLimit())
            hnext = grow(h, errMax);
        else
            hnext = 5.0 * h;
        return y5;
    }

    X stepUsed() const
    {
        return hdid;
    }

    X stepSuggested() const
    {
        return hnext;
    }

    void calculateK(X x, OdeSystem y, X h, Derivs derive)
    {
        k[1] = h * derive(x, y);
        k[2] = h * derive(x + a[2]*h, y + b2[1]*k[1]);
        k[3] = h * derive(x + a[3]*h, y + b3[1]*k[1] + b3[2]*k[2]);
        k[4] = h * derive(x + a[4]*h, y + b4[1]*k[1] + b4[2]*k[2] + b4[3]*k[3]);
        k[5] = h * derive(x + a[5]*h, y + b5[1]*k[1] + b5[2]*k[2] + b5[3]*k[3] + b5[4]*k[4]);
        k[6] = h * derive(x + a[6]*h, y + b6[1]*k[1] + b6[2]*k[2] + b6[3]*k[3] + b6[4]*k[4] + b6[5]*k[5]);
    }

    OdeSystem rk4(OdeSystem y)
    {
        return y + d[1]*k[1] + d[2]*k[2] + d[3]*k[3] + d[4]*k[4] + d[5]*k[5] + d[6]*k[6];
    }

    OdeSystem rk5(OdeSystem y)
    {
        return y + c[1]*k[1] + c[2]*k[2] + c[3]*k[3] + c[4]*k[4] + c[5]*k[5] + c[6]*k[6];
    }

    X grow(X h, pl::dec errorRatioMax)
    {
        return safety * h * std::pow(errorRatioMax, pgrow);
    }

    X shrink(X h, pl::dec errorRatioMax)
    {
        return safety * h * std::pow(errorRatioMax, pshrink);
    }

    pl::dec growLimit()
    {
        return std::pow(5.0/safety, 1.0/pgrow);
    }

private:
    std::array<pl::dec, 7> a;
    std::array<pl::dec, 7> c;
    std::array<pl::dec, 7> d;
    std::array<pl::dec, 2> b2;
    std::array<pl::dec, 3> b3;
    std::array<pl::dec, 4> b4;
    std::array<pl::dec, 5> b5;
    std::array<pl::dec, 6> b6;
    std::array<OdeSystem, 7> k;

    const pl::dec pgrow = 0.2;
    const pl::dec pshrink = 0.25;
    const pl::dec safety = 0.8;
    const pl::dec errcon = std::pow(5.0/safety, 1.0/pgrow);
    pl::dec eps = 1.0E-06;

    X hdid, hnext;

    std::valarray<pl::dec> flatify(const OdeSystem& v)
    {
        auto y = std::get<0>(v);
        auto dy = std::get<1>(v);
        return std::valarray{ {
                y.i().val, y.j().val, y.k().val,
                dy.i().val, dy.j().val, dy.k().val } };
    }
};

rk54::OdeSystem operator*(rk54::X lhs, rk54::ResSystem rhs)
{
    auto y = std::get<0>(rhs);
    auto dy = std::get<1>(rhs);
    return rk54::OdeSystem{ lhs * y, lhs * dy };
}

rk54::ResSystem operator*(pl::dec lhs, rk54::ResSystem rhs)
{
    return rk54::ResSystem{ lhs * std::get<0>(rhs), lhs * std::get<1>(rhs) };
}

rk54::OdeSystem operator*(pl::dec lhs, rk54::OdeSystem rhs)
{
    return rk54::OdeSystem{ lhs * std::get<0>(rhs), lhs * std::get<1>(rhs) };
}

rk54::OdeSystem operator+(rk54::OdeSystem lhs, rk54::OdeSystem rhs)
{
    auto ya = std::get<0>(lhs);
    auto yb = std::get<0>(rhs);
    auto dya = std::get<1>(lhs);
    auto dyb = std::get<1>(rhs);
    return rk54::OdeSystem{ ya + yb, dya + dyb };
}


//template < class UY, class UX, size_t orde=2 >
//class rk54
//{
//public:
//    static_assert(pl::Is_unit<UY>(), "Requires UY as Unit-type");
//    static_assert(pl::Is_unit<UX>(), "Requires UX as Unit-type");
//    using X = pl::Quantity<UX>;

//    struct ODETypes
//    {
//        using y = UY;
//        using dy = pl::Enable_if< std::greater(orde, 1), pl::Unit_minus< UY, UX > >;
//        using d2y = pl::Enable_if< std::greater(orde, 2), pl::Unit_minus< dy, UX > >;
//        using d3y = pl::Enable_if< std::greater(orde, 3), pl::Unit_minus< d2y, UX > >;
//        using d4y = pl::Enable_if< std::greater(orde, 4), pl::Unit_minus< d3y, UX > >;
//    };

//    template < class U >
//    using ResType = pl::Unit_minus< U, UX >;
//    template < class U >
//    using Deriv = std::function< pl::Vector<ResType<U>>( X, pl::Vector<U> ) >;

//    using Y = std::tuple<
//        pl::Vector< ODETypes::y >,
//        pl::Vector< ODETypes::dy >,
//        pl::Vector< ODETypes::d2y >,
//        pl::Vector< ODETypes::d3y >,
//        pl::Vector< ODETypes::d4y >
//    >;

//    using Derivs = std::tuple<
//        Deriv< ODETypes::y >,
//        Deriv< ODETypes::dy >,
//        Deriv< ODETypes::d2y >,
//        Deriv< ODETypes::d3y >,
//        Deriv< ODETypes::d4y >
//    >;

//    struct Result
//    {
//        X hdid, hnext;
//        VecY y;
//    };

//    rk54()
//    {
//        a = { 0.0, 0.0, 0.2, 0.3, 3.0/5.0, 1, 7.0/8.0 };
//        c = { 0.0, 37.0/378, 0, 250.0/621, 125.0/594, 0, 512.0/1771};
//        d = { 0.0, 2825.0/27648, 0, 18575.0/48384, 13525.0/55296, 277.0/14336, 0.25 };
//        b2 = { 0.0, 0.2 };
//        b3 = { 0.0, 3.0/40, 9.0/40 };
//        b4 = { 0.0, 0.3, -0.9, 1.2 };
//        b5 = { 0.0, -11.0/54, 2.5, -70.0/27, 35.0/27 };
//        b6 = { 0.0, 1631.0/55296, 175.0/512, 575.0/13824, 44275.0/110592, 253.0/4096 };
//    }

//    Result operator()(X x, VecY y, X htry, std::function< VecR(X, VecY) > derive,
//                      pl::dec tolerance=1.0E-06)
//    {
//        Result res;
//        eps = tolerance;
//        X h = htry;
//        auto crit = errorCriteria(x, y, h, derive, eps);
//        calculateK(x, y, h, derive);
//        VecY y4 = rk4(y);
//        VecY y5 = rk5(y);
//        auto err = y5 - y4;
//        auto errRatio = pl::abs(crit / err);
//        auto errMax = this->max(errRatio).val;

//        while (errMax <= 1.0)
//        {
//            auto htemp = shrink(h, errMax);
//            h = (h >= X{ 0.0 }) ? std::max(htemp, 0.1 * h) : std::min(htemp, 0.1 * h);
//            if (x+h - x < X{ 1.0E-30 })
//                throw std::underflow_error("Underflow error, stepsize too small");

//            calculateK(x, y, h, derive);
//            y4 = rk4(y);
//            y5 = rk5(y);
//            err = y5 - y4;
//            crit = errorCriteria(x, y, h, derive, eps);
//            errRatio = pl::abs(crit / err);
//            errMax = this->max(errRatio).val;
//        }

//        res.hdid = h;
//        res.y = y5;
//        res.hnext = h;
////        if (errMax < errcon)
////            res.hnext = grow(h, errMax);
////        else
////            res.hnext = 5.0 * h;
//        return res;
//    }

//    void calculateK(X x, VecY y, X h, std::function< VecR(X, VecY) > derive)
//    {
//        k[1] = h * derive(x, y);
//        k[2] = h * derive(x + a[2]*h, y + b2[1]*k[1]);
//        k[3] = h * derive(x + a[3]*h, y + b3[1]*k[1] + b3[2]*k[2]);
//        k[4] = h * derive(x + a[4]*h, y + b4[1]*k[1] + b4[2]*k[2] + b4[3]*k[3]);
//        k[5] = h * derive(x + a[5]*h, y + b5[1]*k[1] + b5[2]*k[2] + b5[3]*k[3] + b5[4]*k[4]);
//        k[6] = h * derive(x + a[6]*h, y + b6[1]*k[1] + b6[2]*k[2] + b6[3]*k[3] + b6[4]*k[4] + b6[5]*k[5]);
//    }

//    VecY rk4(VecY y)
//    {
//        return y + d[1]*k[1] + d[2]*k[2] + d[3]*k[3] + d[4]*k[4] + d[5]*k[5] + d[6]*k[6];
//    }

//    VecY rk5(VecY y)
//    {
//        return y + c[1]*k[1] + c[2]*k[2] + c[3]*k[3] + c[4]*k[4] + c[5]*k[5] + c[6]*k[6];
//    }

//    virtual VecY errorCriteria(X x, VecY y, X h, std::function< VecR(X, VecY) > derive,
//                               pl::dec tolerance=1.0E-06)
//    {
//        return tolerance * (pl::abs(y) + pl::abs(h * derive(x, y)));
//    }

//    pl::Quantity<pl::dimless> max(const pl::Vector<pl::dimless>& y)
//    {
//        auto max = y.i();
//        if (y.j() > max) max = y.j();
//        if (y.k() > max) max = y.k();
//        return max;
//    }

//    X grow(X h, pl::dec errorRatioMax)
//    {
//        return safety * h * std::pow(errorRatioMax, pgrow);
//    }

//    X shrink(X h, pl::dec errorRatioMax)
//    {
//        return safety * h * std::pow(errorRatioMax, pshrink);
//    }

//    pl::dec growLimit()
//    {
//        return std::pow(5.0/safety, 1.0/pgrow);
//    }

//private:
//    std::array<pl::dec, 7> a;
//    std::array<pl::dec, 7> c;
//    std::array<pl::dec, 7> d;
//    std::array<pl::dec, 2> b2;
//    std::array<pl::dec, 3> b3;
//    std::array<pl::dec, 4> b4;
//    std::array<pl::dec, 5> b5;
//    std::array<pl::dec, 6> b6;
//    std::array<VecY, 7> k;

//    const pl::dec pgrow = 0.2;
//    const pl::dec pshrink = 0.25;
//    const pl::dec safety = 0.8;
//    const pl::dec errcon = std::pow(5.0/safety, 1.0/pgrow);
//    pl::dec eps = 1.0E-06;
//};

#endif // RK54_H
