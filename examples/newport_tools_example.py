from oe_tools import newport_tools

power_meter = newport_tools.power_meter()

if __name__ == '__main__':
    wavelength = 500
    display = 'This is measured at 500nm'
    power_meter.read(wavelength, display)