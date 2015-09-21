#include "application.h"
using namespace std;
using namespace pl;
using namespace pl::literals;

/*!
  * \class Application
  * \brief Application logic of charged particle motion simulation.
  *
  * This is a helper class to set up Simulator from console and to print
  * output.
  *
  * We provided two ways to run the simulation. The first one is by providing
  * input file and pipe output to a file, for example:
  *     DTESim < input.dat | output.dat
  *
  * The second one is using build and run approach. The whole application was
  * solely made from standard library, so user only need most recent C++
  * compiler (tested on GCC 4.9.2). To use build and run approach, create a
  * pl::Simulator in main function, set it's parameter then bind it to
  * Application class. Example:
  * \code
  *     #include "simulator.h"
  *     #include "fields.h"
  *     #include "application.h"
  *     using namespace pl;
  *     using namespace pl::literals;
  *
  *     int main()
  *     {
  *         Simulator sim;
  *         sim.setTemperature(15);
  *         sim.setSkip(10000);
  *
  *         SmoothZField field;
  *         field.setBaseValue(4.7_tesla);
  *         field.setGradientZ(0.5);
  *         field.setGradientXY(0.5);
  *         sim.setMagneticField(field);
  *
  *         Application app;
  *         app.bindSimulator(sim);
  *         app.writeOutputHeader();
  *         sim.runUntil(0.001_s);
  *         app.writeOutputFooter();
  *
  *         return 0;
  *     }
  * \endcode
  * After building this code, run the program with:
  *     DTESim | output.dat
  */

/*!
 * \brief Application::prepareSimulator
 * \return simulator object ready to run
 *
 * Prepares simulation through a series of standard console input query. By
 * default this function will set Simulator::callback to this object's
 * Application::writeParticleData.
 */
Simulator Application::prepareSimulator()
{
    Simulator sim;
    string mode;
    cin >> mode;
    if (regex_match(mode, regex{"[Rr]esume"}) | regex_match(mode, regex{"[Cc]ontinue"}))
        resumeSimulation(sim);
    else
        prepareParticle(sim);
    prepareMagneticField(sim);
    prepareParameters(sim);

    writeOutputHeader();

    bindSimulator(sim);
    return sim;
}

void Application::prepareParticle(Simulator &sim)
{
    double a, b, c;
    cin >> a >> b >> c;
    sim.setInitialPosition(make_vector<meter>(a, b, c));
    cin >> a;
    sim.setTemperature(a);
}

void Application::resumeSimulation(Simulator &sim)
{
    double a, b, c;
    cin >> a >> b >> c;
    sim.setDeuteriumPosition(make_vector<meter>(a, b, c));
    cin >> a >> b >> c;
    sim.setTritiumPosition(make_vector<meter>(a, b, c));
    cin >> a >> b >> c;
    sim.setElectronPosition(make_vector<meter>(a, b, c));
    cin >> a >> b >> c;
    sim.setDeuteriumVelocity(make_vector<mps>(a, b, c));
    cin >> a >> b >> c;
    sim.setTritiumVelocity(make_vector<mps>(a, b, c));
    cin >> a >> b >> c;
    sim.setElectronVelocity(make_vector<mps>(a, b, c));
}

void Application::prepareMagneticField(Simulator &sim)
{
    double a, b, c;
    string codename;
    cin >> codename;
    if (regex_match(codename, regex{"[Dd]rift"}))
    {
        GradientZField field;
        cin >> a;
        field.setBaseValue(make_quantity<tesla>(a));
        cin >> a;
        field.setGradient(a);
        sim.setMagneticField(field);
    }
    else if (regex_match(codename, regex{"[Ss]mooth"}))
    {
        SmoothZField field;
        cin >> a;
        field.setBaseValue(make_quantity<tesla>(a));
        cin >> a;
        field.setGradientZ(a);
        cin >> a;
        field.setGradientXY(a);
        sim.setMagneticField(field);
    }
    else if (regex_match(codename, regex{"[Ss]harp"}))
    {
        SharpZField field;
        cin >> a;
        field.setBz0(make_quantity<tesla>(a));
        cin >> a;
        field.setAlpha(a);
        cin >> a;
        field.setBeta(a);
        cin >> a;
        field.setL(a);
        sim.setMagneticField(field);
    }
    else if (regex_match(codename, regex{"[Ss]ine"}))
    {
        SineZField field;
        cin >> a;
        field.setBz0(make_quantity<tesla>(a));
        cin >> a;
        field.setAlpha(a);
        cin >> a;
        field.setBetaMax(a);
        cin >> a;
        field.setL(a);
        cin >> a;
        field.setN(a);
        sim.setMagneticField(field);
    }
    else if (regex_match(codename, regex{"[Hh]elix"}))
    {
        ModHelixField field;
        cin >> a;
        field.setBz0(make_quantity<tesla>(a));
        cin >> a;
        field.setBteta0(make_quantity<tesla>(a));
        cin >> a;
        field.setAlpha(a);
        cin >> a;
        field.setBeta(a);
        cin >> a;
        field.setGamma(a);
        cin >> a;
        field.setL(a);
        cin >> a;
        field.setN(a);
        sim.setMagneticField(field);
    }
    else
    {
        UniformField<tesla> field;
        cin >> a >> b >> c;
        field.setValue(make_vector<tesla>(a, b, c));
        sim.setMagneticField(field);
    }
}

void Application::prepareParameters(Simulator &sim)
{
    double a;
    cin >> a;
    sim.setTimestep(make_quantity<second>(a));
    size_t N;
    cin >> N;
    sim.setSkip(N);
}

void Application::bindSimulator(Simulator &sim)
{
    sim.setCallback([this](const Simulator& s) { writeParticleData(s); });
}

void Application::writeOutputHeader()
{
    cout << "# SIMULATION OF CHARGED PARTICLE MOTION WITHIN MAGNETIC FIELD\n";
    auto date = chrono::system_clock::now();
//    auto time = chrono::system_clock::to_time_t(date);
//    cout << "# Started at " << std::put_time(localtime(&time), "%F %T") << "\n";
    cout << "# Output written as space separated value, with format:\n";
    cout << "time(s) vx_D(m/s) vy_D(m/s) vz_D(m/s) vx_T(m/s) vy_T(m/s) vz_T(m/z) vx_e(m/s) vy_e(m/s) vz_e(m/s)"
         << " x_D(m) y_D(m) z_D(m) x_T(m) y_T(m) z_T(m) x_e(m) y_e(m) z_e(m)\n";
    started = date;
}

template< class U >
void printVector(const Vector<U>& vec)
{
    cout << scientific << vec.i().val << " " << vec.j().val << " " << vec.k().val << " ";
}

void Application::writeParticleData(const Simulator &sim)
{
    auto vD = sim.deuteriumVelocity();
    auto vT = sim.tritiumVelocity();
    auto ve = sim.electronVelocity();
    auto pD = sim.deuteriumPosition();
    auto pT = sim.tritiumPosition();
    auto pe = sim.electronPosition();

    cout << sim.time().val << " ";
    printVector(vD);
    printVector(vT);
    printVector(ve);
    printVector(pD);
    printVector(pT);
    printVector(pe);
    cout << "\n";
}

void Application::writeOutputFooter()
{
    auto date = chrono::system_clock::now();
//    auto time = chrono::system_clock::to_time_t(date);
//    cout << "# Simulation ended at " << std::put_time(localtime(&time), "%F %T") << "\n";
    auto elapsed = chrono::duration_cast<chrono::milliseconds>(date - started);
    cout << "# Elapsed time: " << showpoint << elapsed.count() << " ms \n";
}
