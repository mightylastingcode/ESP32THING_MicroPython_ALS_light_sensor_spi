'''
	Project: SPI Light Sensor using hardwareware spi driver (id=2).

	version 3: change software version to hardware version
	           use 80Mhz instead of 200k hz
'''

import machine
import sys
import utime

from machine import Pin, SPI


class LIGHT_Sensor:
	'''
	Represents a light sensor
	'''
	def __init__(self,freq,port,csbpin,sckpin=18,mosipin=23,misopin=19):
		self.csb  = machine.Pin(csbpin, machine.Pin.OUT)
		self.csb.value(1)   # disable

		# construct an SPI bus on the given pins
		# polarity is the idle state of SCK
		# phase=0 means sample on the first edge of SCK, phase=1 means the second
		# 1M, 10M, 20M ok (1M is more stable)
		if (port == 1):
			self.spi = SPI(1, baudrate=freq, polarity=1, phase=1, bits=8, firstbit=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
		elif (port == 2):
			self,spi = SPI(2, baudrate=freq, polarity=1, phase=1, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
		else:
			self.spi = SPI(baudrate=freq, polarity=1, phase=1, sck=Pin(sckpin), mosi=Pin(mosipin), miso=Pin(misopin))	# software spi

	def get_light_sensor_data(self):
		#print ("Read 2 bytes from SPI light sensor.")
		self.csb.value(0)   # enable
		buf = self.spi.read(2)            # read 2 bytes on MISO 
		self.csb.value(1)   # disable

		print ("Raw Data from the sensor:")
		for x in buf:
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

'''
# place this section in the main.py.

import machine
import sys
import utime
from machine import Pin, I2C

from light_sensor import LIGHT_Sensor

# Pin definitions
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

light_sensor_obj = LIGHT_Sensor(freq = 1000000, port = 1, csbpin = 15)
light_sensor_data = light_sensor_obj.get_light_sensor_data()
print ("Light sensor data = %d" % light_sensor_data)
utime.sleep_ms(100)
# Wait for button 0 to be pressed, and then exit
while True:
    if repl_button.value() == 0:
        print("Dropping to REPL now")
        sys.exit()
    else:
		light_sensor_data = light_sensor_obj.get_light_sensor_data()
		print ("Light sensor data = %d" % light_sensor_data)
		utime.sleep_ms(100)

'''

