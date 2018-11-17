

class WulInterface:
    class __WulInterface:

        def __init__(self, port):
            import smbus
            self.port = port
            self.device = smbus.SMBus(port)

        def __str__(self):
            return repr(self) + self.val

        @staticmethod
        def parse_int(num):
            low = num & 0x00FF
            high = (num & 0xFF00) >> 8
            return [high, low]

        def led_control(self, led_nr, brightness, delay):
            self.device.write_i2c_block_data(0x32, 0x01, [led_nr])
            self.device.write_i2c_block_data(0x32, 0x02, self.parse_int(brightness))
            self.device.write_i2c_block_data(0x32, 0x04, self.parse_int(delay))

            self.device.write_i2c_block_data(0x32, 0x00, [0xFF])  # Flush

        def toggle(self):
            print("I2C: Schreiben auf Device 0x{:02X}".format(self.port))
            try:
                self.device.write_i2c_block_data(0x32, 0x00, [0x1])
            except IOError as err:
                print("Fehler beim Schreiben auf Device 0x{:02X}".format(self.port))

    instance = None

    def __init__(self, port):
        if not WulInterface.instance:
            WulInterface.instance = WulInterface.__WulInterface(port)

    def __getattr__(self, name):
        return getattr(self.instance, name)
