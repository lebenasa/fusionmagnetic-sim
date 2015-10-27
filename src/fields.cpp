#include "fields.h"
using namespace std;
using namespace pl;
using namespace pl::literals;

namespace {
double pi = acos(-1.0);
}

GradientZField::GradientZField(const Vector<tesla> &val, pl::dec grad)
    : alpha{ make_quantity<alphatype>(grad) }, m_B{ val }
{

}

Vector<tesla> GradientZField::operator()(const Vector<meter>& position)
{
	auto Bx = 0.0_tesla;
	auto By = 0.0_tesla;
    auto Bz = m_B.k() * (1.0 + alpha * hypot(position.i(), position.j()));
    //auto Bz = m_B.k() * (1.0 + alpha * position.i());
    return Vector<tesla>{ Bx, By, Bz };
}

void GradientZField::setBaseValue(const Vector<tesla>& val)
{
    m_B = val;
}

Vector<tesla> GradientZField::baseValue() const
{
    return m_B;
}

void GradientZField::setGradient(const pl::dec& grad)
{
    alpha = make_quantity<alphatype>(grad);
}

Quantity<GradientZField::alphatype> GradientZField::gradient() const
{
    return alpha;
}

SmoothZField::SmoothZField(const Quantity<tesla> &Bz0, pl::dec gradZ, pl::dec gradXY)
    : alpha{ make_quantity<alphatype>(gradZ) }, beta { make_quantity<betatype>(gradXY) }, m_Bz0{ Bz0 }
{
}

Vector<tesla> SmoothZField::operator()(const Vector<meter>& position)
{
    auto Bx = -0.5 * m_Bz0 * beta * position.i() * position.k();
    auto By = -0.5 * m_Bz0 * beta * position.j() * position.k();
    auto Bz = m_Bz0 * (1.0 + alpha * hypot(position.i(), position.j()) + beta * position.k() * position.k());
    return Vector<tesla>{ Bx, By, Bz };
}

void SmoothZField::setBaseValue(const Quantity<tesla>& Bz0)
{
    m_Bz0 = Bz0;
}

Quantity<tesla> SmoothZField::baseValue() const
{
    return m_Bz0;
}

void SmoothZField::setGradientZ(const pl::dec& grad)
{
    alpha = make_quantity<alphatype>(grad);
}

Quantity<SmoothZField::alphatype> SmoothZField::gradientZ() const
{
    return alpha;
}

void SmoothZField::setGradientXY(const pl::dec& grad)
{
    beta = make_quantity<betatype>(grad);
}

Quantity<SmoothZField::betatype> SmoothZField::gradientXY() const
{
    return beta;
}

SharpZField::SharpZField(const Quantity<tesla> &Bz0, pl::dec gradZ, pl::dec gradXY)
    : m_Bz0{ Bz0 }, m_alpha{ gradZ }, m_beta{ gradXY }
{
}

Vector<tesla> SharpZField::operator()(const Vector<meter>& position)
{
    Quantity<gradtype> beta;
    if (position.k() > -1.0*m_L && position.k() < m_L)
        beta = make_quantity<gradtype>(0.0);
    else if (position.k() <= -1.0*m_L)
        beta = -1.0*m_beta;
    else
        beta = m_beta;

    auto Bx = -0.5 * m_Bz0 * beta * position.i();
    auto By = -0.5 * m_Bz0 * beta * position.j();
    auto Bz = m_Bz0 * (1.0 + m_alpha * hypot(position.i(), position.j()) + beta * position.k());
    return Vector<tesla>{ Bx, By, Bz };
}

void SharpZField::setBz0(const Quantity<tesla>& Bz0)
{
    m_Bz0 = Bz0;
}

Quantity<tesla> SharpZField::Bz0() const
{
    return m_Bz0;
}

void SharpZField::setAlpha(const pl::dec& v)
{
    m_alpha = make_quantity<gradtype>(v);
}

Quantity<SharpZField::gradtype> SharpZField::alpha() const
{
    return m_alpha;
}

void SharpZField::setBeta(const pl::dec& v)
{
    m_beta = make_quantity<gradtype>(v);
}

Quantity<SharpZField::gradtype> SharpZField::beta() const
{
    return m_beta;
}

void SharpZField::setL(const pl::dec& L)
{
    using namespace pl::literals;
    m_L = L * 1.0_m;
}

Quantity<meter> SharpZField::L() const
{
    return m_L;
}

SineZField::SineZField(const Quantity<tesla> &Bz0, pl::dec gradZ, pl::dec gradXY)
    : m_Bz0{ Bz0 }, m_alpha{ gradZ }, m_beta{ gradXY }
{
}

Vector<tesla> SineZField::operator()(const Vector<meter>& position)
{
	auto npL = m_n * ::pi / m_L;

    auto Bx = -0.5 * m_Bz0 * m_beta * npL * position.i() * std::sin(npL * position.k());
    auto By = -0.5 * m_Bz0 * m_beta * npL * position.j() * std::sin(npL * position.k());
    auto Bz = m_Bz0 * (2.0 + m_alpha * hypot(position.i(), position.j()) - 1.0 * m_beta * std::cos(npL * position.k()));
    return Vector<tesla>{ Bx, By, Bz };
}

void SineZField::setBz0(const Quantity<tesla>& Bz0)
{
    m_Bz0 = Bz0;
}

Quantity<tesla> SineZField::Bz0() const
{
    return m_Bz0;
}

void SineZField::setAlpha(const pl::dec& v)
{
    m_alpha = make_quantity<gradtype>(v);
}

Quantity<SineZField::gradtype> SineZField::alpha() const
{
    return m_alpha;
}

void SineZField::setBetaMax(const pl::dec& v)
{
    m_beta = v;
}

pl::dec SineZField::betaMax() const
{
    return m_beta;
}

void SineZField::setL(const pl::dec& L)
{
    using namespace pl::literals;
    m_L = L * 1.0_m;
}

Quantity<meter> SineZField::L() const
{
    return m_L;
}

void SineZField::setN(const pl::dec &n)
{
    m_n = n;
}

pl::dec SineZField::n() const
{
    return m_n;
}

HelixField::HelixField(const pl::Quantity<tesla> &Bz0, const pl::Quantity<tesla> &Bteta0, pl::dec alpha, pl::dec L, pl::dec n)
    : m_Bz0{ Bz0 }, m_Bt0{ Bteta0 }, m_alpha{ alpha }, m_L{ L }, m_n{ n }
{

}

Vector<tesla> HelixField::operator()(const Vector<meter>& position)
{
    auto r = hypot(position.i(), position.j());
    auto teta = std::atan(position.j().val / position.i().val);
    auto Bteta = m_Bt0 * (1.0 + m_alpha * r);
//    auto Br = ( m_n * ::pi * r / (2.0 * m_L) ) * m_Bz0 * sin(m_n * ::pi * position.k() / m_L);
    auto Br = -1.0 * m_Bz0 * m_beta * r;
    auto Bx = Br * cos(teta) - Bteta * sin(teta);
    auto By = Br * sin(teta) + Bteta * cos(teta);
//    auto Bz = m_Bz0 * cos(m_n * ::pi * position.k() / m_L);
    auto Bz = m_Bz0 * (1 + m_alpha * position.i() + m_beta * position.k());
    return Vector<tesla>{ Bx, By, Bz };
}

void HelixField::setBz0(const pl::Quantity<tesla> &Bz0)
{
    m_Bz0 = Bz0;
}

Quantity<tesla> HelixField::Bz0() const
{
    return m_Bz0;
}

void HelixField::setBteta0(const pl::Quantity<tesla> &Bteta0)
{
    m_Bt0 = Bteta0;
}

Quantity<tesla> HelixField::Bteta0() const
{
    return m_Bt0;
}

void HelixField::setAlpha(const pl::dec &v)
{
    m_alpha = make_quantity<gradtype>(v);
}

Quantity<HelixField::gradtype> HelixField::alpha() const
{
    return m_alpha;
}

void HelixField::setBeta(const pl::dec &v)
{
    m_beta = make_quantity<gradtype>(v);
}

pl::dec HelixField::beta() const
{
    return m_beta.val;
}

void HelixField::setL(const pl::dec &L)
{
    m_L = make_quantity<meter>(L);
}

Quantity<meter>  HelixField::L() const
{
    return m_L;
}

void HelixField::setN(const pl::dec &v)
{
    m_n = v;
}

pl::dec HelixField::n() const
{
    return m_n;
}

ModHelixField::ModHelixField(const pl::Quantity<pl::tesla>& Bz0, const pl::Quantity<pl::tesla>& Bteta0, pl::dec alpha, pl::dec L, pl::dec n)
    : m_Bz0{ Bz0 }, m_Bt0{ Bteta0 }, m_alpha{ alpha }, m_L{ L }, m_n{ n }
{

}

pl::Vector<pl::tesla> ModHelixField::operator()(const pl::Vector<pl::meter>& position)
{
    auto x = position.i(); auto y = position.j(); auto z = position.k();
    auto r = hypot(x, y);
    auto teta = std::atan(y.val / x.val);
    auto Bteta = m_Bt0 * (1.0 + m_gamma * r);
//    auto Br = - 0.5 * m_Bz0 * beta_max * r * (cos(m_n * ::pi * z / m_L) - (m_n * ::pi * z / m_L) * sin(m_n * ::pi * z / m_L));
//    auto Br = m_Bz0 * (m_n * ::pi / m_L) * sin(m_n * ::pi * z / m_L) * (r/2.0 + m_alpha * r * r / 3);
    auto Br = -1.0 * m_Bz0 * m_beta * (m_n * ::pi * r / (2.0 * m_L)) * abs(sin(m_n * ::pi * z / m_L));
    auto Bx = Br * cos(teta) - Bteta * sin(teta);
    auto By = Br * sin(teta) + Bteta * cos(teta);
//    auto Bz = m_Bz0 * (1.0 + m_alpha * r + beta_max * z * cos(m_n * ::pi * z / m_L));
//    auto Bz = m_Bz0 * cos(m_n * ::pi * z / m_L) * (1.0 + m_alpha * r);
    auto Bz = m_Bz0 * (1.0 + m_alpha * r - (m_beta * cos(m_n * ::pi * z / m_L)));
    return Vector<tesla>{ Bx, By, Bz };
}

Quantity<tesla> ModHelixField::radialField(const pl::Vector<meter> &position)
{
    auto x = position.i(); auto y = position.j(); auto z = position.k();
    auto r = hypot(x, y);
    auto Br = -1.0 * m_Bz0 * m_beta * (m_n * ::pi * r / (2.0 * m_L)) * abs(sin(m_n * ::pi * z / m_L));
    return Br;
}

Quantity<tesla> ModHelixField::angularField(const pl::Vector<meter> &position)
{
    auto x = position.i(); auto y = position.j();
    auto r = hypot(x, y);
    auto Bteta = m_Bt0 * (1.0 + m_gamma * r);
    return Bteta;
}

void ModHelixField::setBz0(const pl::Quantity<pl::tesla>& Bz0)
{
    m_Bz0 = Bz0;
}

Quantity<tesla> ModHelixField::Bz0() const
{
    return m_Bz0;
}

void ModHelixField::setBteta0(const pl::Quantity<tesla> &Bteta0)
{
    m_Bt0 = Bteta0;
}

Quantity<tesla> ModHelixField::Bteta0() const
{
    return m_Bt0;
}

void ModHelixField::setAlpha(const pl::dec &v)
{
    m_alpha = make_quantity<gradtype>(v);
}

Quantity<ModHelixField::gradtype> ModHelixField::alpha() const
{
    return m_alpha;
}

void ModHelixField::setBeta(const pl::dec &v) {
    m_beta = make_quantity<dimless>(v);
}

pl::dec ModHelixField::beta() const
{
    return m_beta;
}

void ModHelixField::setGamma(const pl::dec &v) {
    m_gamma = make_quantity<gradtype>(v);
}

Quantity<ModHelixField::gradtype> ModHelixField::gamma() const
{
    return m_gamma;
}

void ModHelixField::setL(const pl::dec &L)
{
    m_L = make_quantity<meter>(L);
}

Quantity<meter>  ModHelixField::L() const
{
    return m_L;
}

void ModHelixField::setN(const pl::dec &v)
{
    m_n = v;
}

pl::dec ModHelixField::n() const
{
    return m_n;
}

// TokamakField
pl::Vector<pl::tesla> TokamakField::operator()(const pl::Vector<pl::meter>& position)
{
    auto x = position.i(); auto y = position.j(); auto z = position.k();
    auto r = hypot(x, y);
    auto teta = std::atan(y.val / x.val);
    auto Bteta = m_Bt0 * (1.0 + m_rho * r);
    auto Br = -1.0 * m_Bz0 * m_gamma * (m_n * ::pi * r / (2.0 * m_L)) * sin(m_n * ::pi * z / m_L) *
            (1.0 + m_epsilon * cos(teta));
    auto Bx = Br * cos(teta) - Bteta * sin(teta);
    auto By = Br * sin(teta) + Bteta * cos(teta);
    auto Bz = m_Bz0 * (1.0 + pl::sqrt(m_alpha * pl::pow<meter, 2>(x) + m_beta * pl::pow<meter, 2>(y)) -
                       (m_gamma * cos(m_n * ::pi * z / m_L))) * (1.0 + m_epsilon * cos(teta));
    return Vector<tesla>{ Bx, By, Bz };
}

void TokamakField::setBz0(const pl::Quantity<pl::tesla>& Bz0)
{
    m_Bz0 = Bz0;
}

Quantity<tesla> TokamakField::Bz0() const
{
    return m_Bz0;
}

void TokamakField::setBteta0(const pl::Quantity<tesla> &Bteta0)
{
    m_Bt0 = Bteta0;
}

Quantity<tesla> TokamakField::Bteta0() const
{
    return m_Bt0;
}

void TokamakField::setAlpha(const pl::dec &v)
{
    m_alpha = make_quantity<TokamakField::GradientAB>(v);
}

Quantity<TokamakField::GradientAB> TokamakField::alpha() const
{
    return m_alpha;
}

void TokamakField::setBeta(const pl::dec &v) {
    m_beta = make_quantity<TokamakField::GradientAB>(v);
}

pl::Quantity<TokamakField::GradientAB> TokamakField::beta() const
{
    return m_beta;
}

void TokamakField::setGamma(const pl::dec &v) {
    m_gamma = v;
}

pl::dec TokamakField::gamma() const
{
    return m_gamma;
}

void TokamakField::setEpsilon(const pl::dec &v)
{
    m_epsilon = v;
}

pl::dec TokamakField::epsilon() const
{
    return m_epsilon;
}

void TokamakField::setRho(const pl::dec &v)
{
    m_rho = make_quantity<TokamakField::GradientP>(v);
}

Quantity<TokamakField::GradientP> TokamakField::rho() const
{
    return m_rho;
}

void TokamakField::setL(const pl::dec &L)
{
    m_L = make_quantity<meter>(L);
}

Quantity<meter>  TokamakField::L() const
{
    return m_L;
}

void TokamakField::setN(const pl::dec &v)
{
    m_n = v;
}

pl::dec TokamakField::n() const
{
    return m_n;
}
