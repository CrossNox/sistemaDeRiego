from neopixel import *
import time

class ledRingPercentage:
	
	def __init__(self,pinNumber,ledCount=16,freq=800000,dma=5,invert=False,brightness=255):
		self.pinNumber = pinNumber
		self.ledCount = ledCount
		# Create NeoPixel object with appropriate configuration.
		self.strip = Adafruit_NeoPixel(ledCount, pinNumber, freq, dma, invert, brightness)
		self.strip.begin()
		
	def showPercentage(self,value,r=0,g=0,b=255):
		pixelsNumber = value*self.ledCount/100.0
		onPixels = int(pixelsNumber)
		lastPixelRChannelValue = int((pixelsNumber - int(pixelsNumber))*r)
		lastPixelGChannelValue = int((pixelsNumber - int(pixelsNumber))*g)
		lastPixelBChannelValue = int((pixelsNumber - int(pixelsNumber))*b)		
		for i in xrange(onPixels):
			self.strip.setPixelColor(i,Color(r,g,b))
		if(onPixels<16):
			self.strip.setPixelColor(onPixels,Color(lastPixelRChannelValue,lastPixelGChannelValue,lastPixelBChannelValue))
		self.strip.show()	
	
	def clear(self):
		for i in xrange(self.ledCount):
			self.strip.setPixelColor(i,Color(0,0,0))
		self.strip.show()

