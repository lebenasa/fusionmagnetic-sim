#ifndef FIELDS_H
#define FIELDS_H
// Variations of magnetic field shape

#include "simulation.hpp"

class GradientZField
{
    using alphatype = pl::Unit_minus<pl::dimless, pl::meter>;
    pl::Quantity<alphatype> alpha;
    pl::Vector<pl::tesla> m_B;
public:
    GradientZField() = default;
    GradientZField(const pl::Vector<pl::tesla>& val, pl::dec grad = 0.5);

    pl::Vector<pl::tesla> operator()(const pl::Vector<pl::meter>& position);

    void setBaseValue(const pl::Vector<pl::tesla>& val);
    pl::Vector<pl::tesla> baseValue() const;
    void setGradient(const pl::dec& grad);
    pl::Quantity<alphatype> gradient() const;
};

class SmoothZField
{
    using alphatype = pl::Unit_minus<pl::dimless, pl::meter>;
    using betatype = pl::Unit_minus<pl::tesla, pl::Unit_plus<pl::meter, pl::meter>>;
    pl::Quantity<alphatype> alpha;
    pl::Quantity<betatype> beta;
    pl::Quantity<pl::tesla> m_Bz0;
public:
    SmoothZField() = default;
    SmoothZField(const pl::Quantity<pl::tesla>& Bz0, pl::dec gradZ, pl::dec gradXY);

    pl::Vector<pl::tesla> operator()(const pl::Vector<pl::meter>& position);

    void setBaseValue(const pl::Quantity<pl::tesla>& Bz0);
    pl::Quantity<pl::tesla> baseValue() const;
    void setGradientZ(const pl::dec& grad);
    pl::Quantity<alphatype> gradientZ() const;
    void setGradientXY(const pl::dec& grad);
    pl::Quantity<betatype> gradientXY() const;
};

class SharpZField
{
    using gradtype = pl::Unit_minus<pl::dimless, pl::meter>;
    pl::Quantity<pl::tesla> m_Bz0;
    pl::Quantity<gradtype> m_alpha;
    pl::Quantity<gradtype> m_beta;
    pl::Quantity<pl::meter> m_L;
public:
    SharpZField() = default;
    SharpZField(const pl::Quantity<pl::tesla>& Bz0, pl::dec gradZ, pl::dec gradXY);

    pl::Vector<pl::tesla> operator()(const pl::Vector<pl::meter>& position);

    void setBz0(const pl::Quantity<pl::tesla>& Bz0);
    pl::Quantity<pl::tesla> Bz0() const;
    void setAlpha(const pl::dec& v);
    pl::Quantity<gradtype> alpha() const;
    void setBeta(const pl::dec& v);
    pl::Quantity<gradtype> beta() const;
    void setL(const pl::dec& L);
    pl::Quantity<pl::meter> L() const;
};

class SineZField
{
    using gradtype = pl::Unit_minus<pl::dimless, pl::meter>;
    pl::Quantity<pl::tesla> m_Bz0;
    pl::Quantity<gradtype> m_alpha;
    pl::Quantity<gradtype> m_beta;
    pl::Quantity<pl::meter> m_L;
    pl::dec m_n;
public:
    SineZField() = default;
    SineZField(const pl::Quantity<pl::tesla>& Bz0, pl::dec gradZ, pl::dec gradXY);

    pl::Vector<pl::tesla> operator()(const pl::Vector<pl::meter>& position);

    void setBz0(const pl::Quantity<pl::tesla>& Bz0);
    pl::Quantity<pl::tesla> Bz0() const;
    void setAlpha(const pl::dec& v);
    pl::Quantity<gradtype> alpha() const;
    void setBetaMax(const pl::dec& v);
    pl::Quantity<gradtype> betaMax() const;
    void setL(const pl::dec& L);
    pl::Quantity<pl::meter> L() const;
    void setN(const pl::dec& n);
    pl::dec n() const;
};

class HelixField
{
    using gradtype = pl::Unit_minus<pl::dimless, pl::meter>;
    pl::Quantity<pl::tesla> m_Bz0, m_Bt0;
    pl::Quantity<gradtype> m_alpha, m_beta;
    pl::Quantity<pl::meter> m_L;
    pl::dec m_n;
public:
    HelixField() = default;
    HelixField(const pl::Quantity<pl::tesla>& Bz0, const pl::Quantity<pl::tesla>& Bteta0, pl::dec alpha = 0.5, pl::dec L = 1.0, pl::dec n = 0);

    pl::Vector<pl::tesla> operator()(const pl::Vector<pl::meter>& position);

    void setBz0(const pl::Quantity<pl::tesla>& Bz0);
    pl::Quantity<pl::tesla> Bz0() const;
    void setBteta0(const pl::Quantity<pl::tesla>& Bteta0);
    pl::Quantity<pl::tesla> Bteta0() const;
    void setAlpha(const pl::dec& v);
    pl::Quantity<gradtype> alpha() const;
    void setBeta(const pl::dec& v);
    pl::dec beta() const;   void setL(const pl::dec& L);
    pl::Quantity<pl::meter> L() const;
    void setN(const pl::dec& v);
    pl::dec n() const;
};

class ModHelixField
{
    using gradtype = pl::Unit_minus<pl::dimless, pl::meter>;
    pl::Quantity<pl::tesla> m_Bz0, m_Bt0;
    pl::Quantity<gradtype> m_alpha, m_gamma;
    pl::dec m_beta;
    pl::Quantity<pl::meter> m_L;
    pl::dec m_n;
public:
    ModHelixField() = default;
    ModHelixField(const pl::Quantity<pl::tesla>& Bz0, const pl::Quantity<pl::tesla>& Bteta0, pl::dec alpha = 0.5, pl::dec L = 1.0, pl::dec n = 0);

    pl::Vector<pl::tesla> operator()(const pl::Vector<pl::meter>& position);

    void setBz0(const pl::Quantity<pl::tesla>& Bz0);
    pl::Quantity<pl::tesla> Bz0() const;
    void setBteta0(const pl::Quantity<pl::tesla>& Bteta0);
    pl::Quantity<pl::tesla> Bteta0() const;
    void setAlpha(const pl::dec& v);
    pl::Quantity<gradtype> alpha() const;
    void setBeta(const pl::dec& v);
    pl::dec beta() const;
    void setGamma(const pl::dec& v);
    pl::Quantity<gradtype> gamma() const;
    void setL(const pl::dec& L);
    pl::Quantity<pl::meter> L() const;
    void setN(const pl::dec& v);
    pl::dec n() const;

    pl::Quantity<pl::tesla> radialField(const pl::Vector<pl::meter>& position);
    pl::Quantity<pl::tesla> angularField(const pl::Vector<pl::meter>& position);
};

class TokamakField
{
    using GradientAB = pl::Unit_minus<pl::dimless, pl::Unit_plus<pl::meter, pl::meter> >;
    using GradientP = pl::Unit_minus<pl::dimless, pl::meter>;
    pl::Quantity<pl::tesla> m_Bz0, m_Bt0;
    pl::Quantity<GradientAB> m_alpha, m_beta;
    pl::dec m_gamma, m_epsilon;
    pl::Quantity<GradientP> m_rho;
    pl::Quantity<pl::meter> m_L;
    pl::dec m_n;
public:
    TokamakField() = default;

    pl::Vector<pl::tesla> operator()(const pl::Vector<pl::meter>& position);

    void setBz0(const pl::Quantity<pl::tesla>& Bz0);
    pl::Quantity<pl::tesla> Bz0() const;
    void setBteta0(const pl::Quantity<pl::tesla>& Bteta0);
    pl::Quantity<pl::tesla> Bteta0() const;
    void setAlpha(const pl::dec& v);
    pl::Quantity<GradientAB> alpha() const;
    void setBeta(const pl::dec& v);
    pl::Quantity<GradientAB> beta() const;
    void setGamma(const pl::dec& v);
    pl::dec gamma() const;
    void setEpsilon(const pl::dec& v);
    pl::dec epsilon() const;
    void setRho(const pl::dec& v);
    pl::Quantity<GradientP> rho() const;
    void setL(const pl::dec& L);
    pl::Quantity<pl::meter> L() const;
    void setN(const pl::dec& v);
    pl::dec n() const;
};

#endif // FIELDS_H
