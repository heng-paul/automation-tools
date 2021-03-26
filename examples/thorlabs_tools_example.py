from oe_tools import thorlabs_tools

platform_serial_no = "45871195"
platform = thorlabs_tools.thorlabs_lts150(platform_serial_no)

if __name__ == '__main__':
    platform.home()
    platform.move_to_position(10)