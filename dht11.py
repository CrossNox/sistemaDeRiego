import Adafruit_DHT
import time

class dht11:
	def __init__(self, pinNumber):
		self.pinNumber = pinNumber
		
	def readHumidity(self):
		val = Adafruit_DHT.read_retry(11,self.pinNumber)[0]
		time.sleep(2)
		return val
		
	def readTemp(self):
		val = Adafruit_DHT.read_retry(11,self.pinNumber)[1]
		time.sleep(2)
		return val
		
	def readHumAndTemp(self):
		val = Adafruit_DHT.read_retry(11,self.pinNumber)
		time.sleep(2)
		return val
