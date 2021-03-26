import win32com.client
import traceback
from time import sleep

class power_meter():

    def __init__(self):
        return None

    def read(self, wavelength, display_string):
        # :param wavelength: Int type that sets up the Laser parameter in the Newport
        try:
            OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
            # Stop & Close all devices
            OphirCOM.StopAllStreams() 
            OphirCOM.CloseAll()
            # Scan for connected Devices
            DeviceList = OphirCOM.ScanUSB()
            print(DeviceList)

            # If any device is connected
            for Device in DeviceList:
                # Open first device
                DeviceHandle = OphirCOM.OpenUSBDevice(Device)
                exists = OphirCOM.IsSensorExists(DeviceHandle, 0)
                if exists:
                    print('\n--------------- Data for iref: {0} ------------------'.format(display_string))
                    
                    # Setup laser parameters
                    OphirCOM.ModifyWavelength(DeviceHandle, 0, 0, wavelength)
                    OphirCOM.SetWavelength(DeviceHandle, 0, 0)

                    # Wait for Newport to get setup
                    # CHANGE THIS IF YOU NEED MORE OR LESS TIME!!!
                    init_time = .005
                    sleep(init_time)

                    #OphirCOM.WaveLength(DeviceHandle, 820)
                    # An Example for data retrieving
                    # Start measuring
                    OphirCOM.StartStream(DeviceHandle, 0)

                    # collecting samples in measured_data to take an average
                    measured_data = []

                    # range(10) was the default
                    # Changing until we get 5 samples that are above 0 so we can average them
                    # for i in range(10):
                    count = 0
                    while len(measured_data) < 5:
                        # This is to keep track how many times we do this
                        count += 1

                        # Wait a little for data
                        wait_time = 0.5
                        sleep(wait_time)
                        data = OphirCOM.GetData(DeviceHandle, 0)

                        # if any data available, print the first one from the batch
                        if len(data[0]) > 0:
                            # Turning measured into non sci notation
                            measured = float(data[0][0]) * 10**6
                            print('Reading = {0} uW'.format(measured))
                            measured_data.append(measured)

                    # Tells the user how the LED was on        
                    total_time = init_time + (wait_time * count)
                    print()
                    print('Total time to gather data: {0}s'.format(total_time))
                    print()
                else:
                    print('\nNo Sensor attached to {0} !!!'.format(Device))    

        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            traceback.print_exc()

        # win32gui.MessageBox(0, 'finished', '', 0)
        # Stop & Close all devices
        OphirCOM.StopAllStreams()
        OphirCOM.CloseAll()

        # Release the object
        OphirCOM = None

        # Returns the average of the measured values and rounds it
        print()
        print('Collected {0} data points'.format(len(measured_data)))
        averaged_measured = round(sum(measured_data) / len(measured_data), 3)
        print('The average power reading is {0}uW for {1}'.format(averaged_measured, display_string))
        print()
        return averaged_measured