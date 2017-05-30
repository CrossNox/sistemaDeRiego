import motor
import ledRingPercentage
import time
import dht11

m = motor.motor(21)
l = ledRingPercentage.ledRingPercentage(12)
d = dht11.dht11(4)

m.turnOn()
for i in range(0,100,6):
	l.showPercentage(i)
	print "H: %.1f, T: %.1f" % d.readHumAndTemp()
l.clear()
m.turnOff()
