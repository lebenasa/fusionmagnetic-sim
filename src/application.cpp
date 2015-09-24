#include "application.h"
using namespace std;
using namespace pl;
using namespace pl::literals;
using namespace pl::constants;

Application::Application()
    : sim{ }, isRunning{ false }
{
    monitor = sim.shareMonitor();
}

void Application::promptParticleData()
{
    // Particle ID:
    // manual, e-, p+, n, De+, Tr+, He+
    int id;
    string name;
    cin >> std::nouppercase >> name;
    if (name == "manual") id = -1;
    else if (name == "e-") id = 0;
    else if (name == "p+") id = 1;
    else if (name == "n") id = 2;
    else if (name == "de+") id = 3;
    else if (name == "tr+") id = 4;
    else if (name == "he+") id = 5;
    else id = -1;
    sim.setParticleId(id);
    if (id == -1)
    {
        double m, c;
        cin >> m >> c;
        auto mass = Quantity<kilogram>{ m };
        auto charge = Quantity<coulomb>{ c };
        sim.setMass(mass > 0.0_kg ? mass : 0.0_kg);
        sim.setCharge(charge);
    }

    // Write stored parameters:
    cout << "# Mass (m)\t\t" << sim.mass().val << " kg\n";
    cout << "# Charge (q)\t\t" << sim.charge().val << " Coulomb\n";
}

void Application::promptInitialCondition()
{
    // Initial position
    double x, y, z;
    cin >> x >> y >> z;
    sim.setInitialPosition(make_vector<meter>(x, y, z));

    // Initial velocity
    // Use plasma temperature? (Y/n)
    char vel_flag;
    cin >> std::uppercase >> vel_flag;
    if (vel_flag == 'Y')
    {
        double k;
        cin >> k;
        sim.setInitialVelocity(Quantity<keV>{ k });
        cout << "# Plasma temperature (Ek)\t" << k << " keV\n";
    }
    else
    {
        double vx, vy, vz;
        cin >> vx >> vy >> vz;
        sim.setInitialVelocity(make_vector<mps>(vx, vy, vz));
    }
}

void Application::promptSimulationParams()
{
    // Initial time, end time and timestep
    double t0, tend, h;
    cin >> t0 >> tend >> h;
    sim.setInitialTime(Quantity<second>{t0});
    sim.setEndTime(Quantity<second>{tend});
    sim.setTimestep(Quantity<second>{h});
}

void Application::promptMagneticField()
{
    // Field codename
    double a, b, c;
    string codename;
    cin >> codename;

    // Field strength
    if (regex_match(codename, regex{"[Dd]rift"}))
    {
        GradientZField field;
        cin >> a;
        field.setBaseValue(make_quantity<tesla>(a));
        cin >> b;
        field.setGradient(b);
        sim.setMagneticField(field);

        cout << "# Field codename: Drift\n";
        cout << "# Base strength\t" << a << " Tesla\n";
        cout << "# Gradient const\t" << b << "\n";
    }
    else if (regex_match(codename, regex{"[Ss]mooth"}))
    {
        SmoothZField field;
        cin >> a;
        field.setBaseValue(make_quantity<tesla>(a));
        cin >> b;
        field.setGradientZ(b);
        cin >> c;
        field.setGradientXY(c);
        sim.setMagneticField(field);

        cout << "# Field codename: Smooth\n";
        cout << "# Base strength\t" << a << " Tesla\n";
        cout << "# Parallel gradient\t" << b << "\n";
        cout << "# Perpendicular gradient\t" << c << "\n";
    }
    else if (regex_match(codename, regex{"[Ss]harp"}))
    {
        SharpZField field;
        cin >> a;
        field.setBz0(make_quantity<tesla>(a));
        cin >> b;
        field.setAlpha(b);
        cin >> c;
        field.setBeta(c);
        double d;
        cin >> d;
        field.setL(d);
        sim.setMagneticField(field);

        cout << "# Field codename: Sharp\n";
        cout << "# Base strength\t" << a << " Tesla\n";
        cout << "# Alpha const\t" << b << "\n";
        cout << "# Beta const\t" << c << "\n";
        cout << "# Dist length (L)\t" << d << " meter\n";
    }
    else if (regex_match(codename, regex{"[Ss]ine"}))
    {
        SineZField field;
        cin >> a;
        field.setBz0(make_quantity<tesla>(a));
        cin >> b;
        field.setAlpha(b);
        cin >> c;
        field.setBetaMax(c);
        double d, e;
        cin >> d;
        field.setL(d);
        cin >> e;
        field.setN(e);
        sim.setMagneticField(field);

        cout << "# Field codename: Sine\n";
        cout << "# Base strength\t" << a << " Tesla\n";
        cout << "# Alpha const\t" << b << "\n";
        cout << "# Beta const\t" << c << "\n";
        cout << "# Dist length (L)\t" << d << " meter\n";
        cout << "# Dist freq (N)\t" << e << "\n";
    }
    else if (regex_match(codename, regex{"[Hh]elix"}))
    {
        ModHelixField field;
        cin >> a;
        field.setBz0(make_quantity<tesla>(a));
        cin >> b;
        field.setBteta0(make_quantity<tesla>(b));
        cin >> c;
        field.setAlpha(c);
        double d, e, f, g;
        cin >> d;
        field.setBeta(d);
        cin >> e;
        field.setGamma(e);
        cin >> f;
        field.setL(f);
        cin >> g;
        field.setN(g);
        sim.setMagneticField(field);

        cout << "# Field codename: Helix\n";
        cout << "# Base strength\t" << a << " Tesla\n";
        cout << "# Poloidal strength\t" << b << " Tesla\n";
        cout << "# Alpha const\t" << c << "\n";
        cout << "# Beta const\t" << d << "\n";
        cout << "# Gamma const\t" << e << "\n";
        cout << "# Dist length (L)\t" << f << " meter\n";
        cout << "# Dist freq (N)\t" << g << "\n";
    }
    else
    {
        UniformField<tesla> field;
        cin >> a >> b >> c;
        field.setValue(make_vector<tesla>(a, b, c));
        sim.setMagneticField(field);

        cout << "# Field codename: Homogen\n";
        cout << "# Base strength\t{" << a << ", " << b << ", " << c
             << "} Tesla\n";
    }
}

void Application::writeOutputHeader()
{
//    auto time = chrono::system_clock::to_time_t(date);
//    cout << "# Started at " << std::put_time(localtime(&time), "%F %T") << "\n";
    cout << "# Output written as space separated value, with format:\n";
    cout << "# time x y z vx vy vz computation_time\n\n";
}

void Application::writeOutputFooter()
{
    auto date = chrono::system_clock::now();
//    auto time = chrono::system_clock::to_time_t(date);
//    cout << "# Simulation ended at " << std::put_time(localtime(&time), "%F %T") << "\n";
    auto elapsed = chrono::duration_cast<chrono::milliseconds>(date - started);
    cout << "# Elapsed time: " << showpoint << elapsed.count() << " ms \n";
    cout << "# ---  END OUTPUT  ---\n";
}

void Application::writeOutput()
{
    using namespace chrono;
    using namespace this_thread;

    auto waitTime = milliseconds{ 1 };
    milliseconds total_wait{ 0 };

    auto write = [&]() {
        auto t = monitor->pullTime();
        auto r = monitor->pullPosition();
        auto v = monitor->pullVelocity();
        auto elapsed = duration_cast<milliseconds>(system_clock::now() - started) -
                total_wait - monitor->stallTime();
//        auto elapsed = duration_cast<milliseconds>(system_clock::now() - started);
        cout << setprecision(5) << scientific
             << t.val << " "
             << r.i().val << " " << r.j().val << " " << r.k().val << " "
             << v.i().val << " " << v.j().val << " " << v.k().val << " "
             << elapsed.count() << "\n";
    };

    while (isRunning)
    {
        if (monitor->isEmpty())
        {
            sleep_for(waitTime);
            total_wait += waitTime;
            continue;
        }
        write();
    }

    cout << "# --- END SIMULATION ---\n";
    while (!monitor->isEmpty())
        write();
}

void Application::exec()
{
    cout << "# --- BEGIN PARAMS ---\n";
    promptParticleData();
    promptInitialCondition();
    promptMagneticField();
    promptSimulationParams();
    cout << "# ---  END PARAMS  ---\n";
    cout << "# \n";
    writeOutputHeader();
    auto date = chrono::system_clock::now();
    started = date;
    isRunning = true;
    cout << "# --- BEGIN SIMULATION ---\n";
    auto writing_future = async(launch::async, [this](){ writeOutput(); });
    sim.run();
    isRunning = false;
    writing_future.get();
    writeOutputFooter();
}
