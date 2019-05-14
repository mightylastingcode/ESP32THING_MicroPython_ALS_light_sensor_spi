'''
	Project: SPI Light Sensor using hardwareware spi driver (id=2).

	version 3: change software version to hardware version
	           use 80Mhz instead of 200k hz
'''

import machine
import sys
import utime

from machine import Pin, SPI

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
csb  = machine.Pin(15, machine.Pin.OUT)
csb.value(1)   # disable

# construct an SPI bus on the given pins
# polarity is the idle state of SCK
# phase=0 means sample on the first edge of SCK, phase=1 means the second
# 1M, 10M, 20M ok (1M is more stable)
spi = SPI(1, baudrate=10000000, polarity=1, phase=1, bits=8, firstbit=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))


def get_light_sensor_data():
	#print ("Read 2 bytes from SPI light sensor.")
	csb.value(0)   # enable
	buf = spi.read(2)            # read 2 bytes on MISO 
	csb.value(1)   # disable

	print ("Raw Data from the sensor:")
	for x in buf
		print ("%x" % x)
	#print ("MSB data")
	data_msb = (buf[0] & 0x1f) <<3
	#print ("%x" % data_msb)  

	#print ("LSB data")
	data_lsb = (buf[1] & 0xe0) >>5
	#print ("%x" % data_lsb)  

	#print ("8 bit sensor data:")
	data = data_msb | data_lsb
	#print ("%x" % data)  
	return data

light_data = get_light_sensor_data()
print ("Light data = %d" % light_data)
utime.sleep_ms(100)
# Wait for button 0 to be pressed, and then exit
while True:
    if repl_button.value() == 0:
        print("Dropping to REPL now")
        sys.exit()
    else:
		light_data = get_light_sensor_data()
		print ("Light data = %d" % light_data)
		utime.sleep_ms(100)


