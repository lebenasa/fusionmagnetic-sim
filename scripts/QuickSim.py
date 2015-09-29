import settings
import magnetic as mag
import utility as util
import plot_utility as putil

constants = {
'atomic_mass': 1.660566E-27,
'elementary_charge': 1.6021892E-19,
'light_speed': 2.9979E08
}

def gyro_freq(mass, charge, magnetic):
    return abs(charge) * magnetic / mass

if __name__ == '__main__':
    s = settings.Settings()
    s.outfile = 'Helix_Fixed4'
    s.save()
    
    app = mag.Application()
    app.x0 = 6.0
    app.y0 = 6.0
    app.z0 = 0.3
    app.useKineticEnergy = True
    app.kineticEnergy = 1500
    app.particleCode = 'de+'
    app.initialTime = 0.0
    app.endTime = 6.0E-5
    mass = 2.013553 * constants['atomic_mass']
    charge = 1.0 * constants['elementary_charge']
    app.timeStep = 0.01 * (1.0 / gyro_freq(mass, charge, 4.7))

    app.fieldCode = 'Helix'
    app.fieldBaseStrength = [ 4.7, 3.0 ]
    app.fieldGradient = [ 0.2, 0.2, 0.5 ]
    app.fieldLength = 1.0
    app.fieldFreq = 1.0
    
    app.save()

    from os import path, remove
    if path.exists(s.outpath()):
        remove(s.outpath())
    
    app.execute()

    success = False
    with open(path.join(s.outdir, s.outfile) + s.outext, 'r') as out:
        for line in out:
            pass
        success = line.find("END OUTPUT") != -1
    print success