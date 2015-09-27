#ifndef RK54_H
#define RK54_H

#include "simulatorlib.hpp"
#include <array>
#include <functional>
#include <vector>
#include <exception>
#include <iostream>

/*!
 * Runge-Kutta Fehlberg implementation
 * Given unit of Y and X as UY and UX, this class will act as function object
 * which returns y(x + h) with built-in adaptive stepsize control.
 * Alternatively, user can build their own adaptive stepsize control by
 * accessing public functions rk4() and rk5(). Note that calculateK must be
 * called before using rk4() and rk5().
 */
template < class UY, class UX >
class rk54
{
public:
    static_assert(pl::Is_unit<UY>(), "Requires UY as Unit-type");
    static_assert(pl::Is_unit<UX>(), "Requires UX as Unit-type");
    using X = pl::Quantity<UX>;
    using Y = pl::Quantity<UY>;
    using UR = pl::Unit_minus<UY, UX>;
    using VecY = pl::Vector<UY>;
    using VecR = pl::Vector<UR>;

    struct Result
    {
        X hdid, hnext;
        VecY y;
    };

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

    Result operator()(X x, VecY y, X htry, std::function< VecR(X, VecY) > derive,
                      pl::dec tolerance=1.0E-06)
    {
        Result res;
        eps = tolerance;
        X h = htry;
        auto crit = errorCriteria(x, y, h, derive, eps);
        calculateK(x, y, h, derive);
        VecY y4 = rk4(y);
        VecY y5 = rk5(y);
        auto err = y5 - y4;
        auto errRatio = pl::abs(crit / err);
        auto errMax = this->max(errRatio).val;

        while (errMax <= 1.0)
        {
            auto htemp = shrink(h, errMax);
            h = (h >= X{ 0.0 }) ? std::max(htemp, 0.1 * h) : std::min(htemp, 0.1 * h);
            if (x+h - x < X{ 1.0E-30 })
                throw std::underflow_error("Underflow error, stepsize too small");

            calculateK(x, y, h, derive);
            y4 = rk4(y);
            y5 = rk5(y);
            err = y5 - y4;
            crit = errorCriteria(x, y, h, derive, eps);
            errRatio = pl::abs(crit / err);
            errMax = this->max(errRatio).val;
        }

        res.hdid = h;
        res.y = y5;
        res.hnext = h;
//        if (errMax < errcon)
//            res.hnext = grow(h, errMax);
//        else
//            res.hnext = 5.0 * h;
        return res;
    }

    void calculateK(X x, VecY y, X h, std::function< VecR(X, VecY) > derive)
    {
        k[1] = h * derive(x, y);
        k[2] = h * derive(x + a[2]*h, y + b2[1]*k[1]);
        k[3] = h * derive(x + a[3]*h, y + b3[1]*k[1] + b3[2]*k[2]);
        k[4] = h * derive(x + a[4]*h, y + b4[1]*k[1] + b4[2]*k[2] + b4[3]*k[3]);
        k[5] = h * derive(x + a[5]*h, y + b5[1]*k[1] + b5[2]*k[2] + b5[3]*k[3] + b5[4]*k[4]);
        k[6] = h * derive(x + a[6]*h, y + b6[1]*k[1] + b6[2]*k[2] + b6[3]*k[3] + b6[4]*k[4] + b6[5]*k[5]);
    }

    VecY rk4(VecY y)
    {
        return y + d[1]*k[1] + d[2]*k[2] + d[3]*k[3] + d[4]*k[4] + d[5]*k[5] + d[6]*k[6];
    }

    VecY rk5(VecY y)
    {
        return y + c[1]*k[1] + c[2]*k[2] + c[3]*k[3] + c[4]*k[4] + c[5]*k[5] + c[6]*k[6];
    }

    virtual VecY errorCriteria(X x, VecY y, X h, std::function< VecR(X, VecY) > derive,
                               pl::dec tolerance=1.0E-06)
    {
        return tolerance * (pl::abs(y) + pl::abs(h * derive(x, y)));
    }

    pl::Quantity<pl::dimless> max(const pl::Vector<pl::dimless>& y)
    {
        auto max = y.i();
        if (y.j() > max) max = y.j();
        if (y.k() > max) max = y.k();
        return max;
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
    std::array<VecY, 7> k;

    const pl::dec pgrow = 0.2;
    const pl::dec pshrink = 0.25;
    const pl::dec safety = 0.8;
    const pl::dec errcon = std::pow(5.0/safety, 1.0/pgrow);
    pl::dec eps = 1.0E-06;
};

#endif // RK54_H
