"Sample code for absolute movement."
from ctypes import (
    c_int,
    c_char_p,
)
from time import sleep

from thorlabs_kinesis import integrated_stepper_motors as ism

if __name__ == "__main__":
    serial_no = c_char_p(bytes("45871195", "utf-8"))
    milliseconds = c_int(100)

    if ism.TLI_BuildDeviceList() == 0:
        err = ism.ISC_Open(serial_no)
        if err == 0:
            print("Starting polling ", ism.ISC_StartPolling(serial_no, milliseconds))
            print("Clearing message queue ", ism.ISC_ClearMessageQueue(serial_no))
            sleep(0.2)

            # Example 77 multplier goes to 77mm
            ten_mm = 409600
            multiplier = 70
            move_to = ten_mm * multiplier
            move_to = int(move_to)

            print("Setting Absolute Position ", ism.ISC_SetMoveAbsolutePosition(serial_no, c_int(move_to)))
            sleep(0.2)

            print("Moving to", move_to, ism.ISC_MoveAbsolute(serial_no))
            sleep(0.2)
            pos = int(ism.ISC_GetPosition(serial_no))
            sleep(0.2)
            print('Current pos:', pos)
            while not pos == move_to:
                sleep(0.2)
                pos = int(ism.ISC_GetPosition(serial_no))
                print("Current pos;", pos)

            print("Stopping polling ", ism.ISC_StopPolling(serial_no))
            print("Closing connection ", ism.ISC_Close(serial_no))
        else:
            print("Can't open. Error:", err)