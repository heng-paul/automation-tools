"Sample code to get hardware information."
from ctypes import (
    c_short,
    c_char_p,
    c_int,
    byref,
)
from time import sleep
from thorlabs_kinesis import integrated_stepper_motors as ism
if __name__ == "__main__":
    serial_no = c_char_p(bytes("45871195", "utf-8"))
    channel = c_short(1)

    if ism.TLI_BuildDeviceList() == 0:
        if ism.ISC_Open(serial_no) == 0:

            ism.ISC_Home(serial_no)
            sleep(10)
            ism.ISC_Close(serial_no)
        else:
            print("Can't open connection.")
    else:
        print("Can't build device list")