#!/usr/bin/python3

import smbus

device = smbus.SMBus(1)

run_count = 0

address = 50
print("I2C: Schreiben auf Device 0x{:02X}".format(address))
try:
	device.write_i2c_block_data(0x32, 0x00, [0x1])

except IOError as err:
	print("Fehler beim Schreiben auf Device 0x{:02X}".format(address))
	exit(-1)


print("Done")



