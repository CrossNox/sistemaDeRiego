import wiringpi as wp

class motor:
	pin = None
	state = 0
	
	def __init__(self, pinNumber):
		self.pin = pinNumber
		if(wp.wiringPiSetup() != 0):
			raise motorInitializationError("Startup failed")
		wp.pinMode(pinNumber,1)
		self._setAndWrite(0)
	
	def _setAndWrite(self,val):
		self.state = val
		wp.digitalWrite(self.pin,self.state)
		
	def toggleState(self):
		self._setAndWrite(1-self.state)	
		
	def turnOff(self):
		self._setAndWrite(0)
	
	def turnOn(self):
		self._setAndWrite(1)
		
	def __del__(self):
		wp.digitalWrite(self.pin,0)
		wp.pinMode(self.pin,0)

class motorInitializationError(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)

