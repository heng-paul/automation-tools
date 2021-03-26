from time import sleep
from thorlabs_kinesis import integrated_stepper_motors as ism
from ctypes import c_int, c_char_p

class thorlabs_lts150():

    def __init__(self, serial_no):
        self.serial_no = serial_no

    def move_to_position(self, position):
        # :param position: Integer type that can be 1 to 150
        # This fuction moves the LTS150 to the given position in mm
        # Credit: https://github.com/ekarademir/thorlabs-kinesis
        serial_no = c_char_p(bytes(self.serial_no, "utf-8"))
        milliseconds = c_int(100)

        # TO DO: Check if the given position aparameter is 1-150mm

        if ism.TLI_BuildDeviceList() == 0:
            err = ism.ISC_Open(serial_no)
            if err == 0:
                print("Starting polling ", ism.ISC_StartPolling(serial_no, milliseconds))
                print("Clearing message queue ", ism.ISC_ClearMessageQueue(serial_no))
                sleep(0.2)

                # Example 77 multplier goes to 77mm
                ten_mm = 409600
                multiplier = position
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

    def home(self):
        # This function moves the LTS150 to the home position
        # Credit: https://github.com/ekarademir/thorlabs-kinesis
        serial_no = c_char_p(bytes(self.serial_no, "utf-8"))
        milliseconds = c_int(100)

        if ism.TLI_BuildDeviceList() == 0:
            if ism.ISC_Open(serial_no) == 0:
                sleep(1.0)
                ism.ISC_StartPolling(serial_no, milliseconds)
                ism.ISC_ClearMessageQueue(serial_no)
                sleep(1.0)

                err = ism.ISC_Home(serial_no)
                sleep(1.0)
                if err == 0:
                    while True:
                        current_pos = int(ism.ISC_GetPosition(serial_no))
                        if current_pos == 0:
                            print("At home.")
                            break
                        else:
                            print("Homing...", current_pos)

                        sleep(1.0)
                else:
                    print("Can't home. Err:", err)

                ism.ISC_StopPolling(serial_no)
                ism.ISC_Close(serial_no)
            else:
                print("Can't open")
        else:
            print("Can't build device list.")