"Sample code for homing."
from ctypes import (
    c_short,
    c_int,
    c_char_p,
)
from time import sleep
import sys 


from thorlabs_kinesis import integrated_stepper_motors as kdc


if __name__ == "__main__":
    serial_no = c_char_p(bytes("45871195", "utf-8"))
    milliseconds = c_int(100)

    if kdc.TLI_BuildDeviceList() == 0:
        if kdc.ISC_Open(serial_no) == 0:
            sleep(1.0)
            kdc.ISC_StartPolling(serial_no, milliseconds)
            kdc.ISC_ClearMessageQueue(serial_no)
            sleep(1.0)

            err = kdc.ISC_Home(serial_no)
            sleep(1.0)
            if err == 0:
                while True:
                    current_pos = int(kdc.ISC_GetPosition(serial_no))
                    if current_pos == 0:
                        print("At home.")
                        break
                    else:
                        print("Homing...", current_pos)

                    sleep(1.0)
            else:
                print("Can't home. Err:", err)

            kdc.ISC_StopPolling(serial_no)
            kdc.ISC_Close(serial_no)
        else:
            print("Can't open")
    else:
        print("Can't build device list.")
