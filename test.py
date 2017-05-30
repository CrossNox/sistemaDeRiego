import motor
import ledRingPercentage
import time

m = motor.motor(21)
l = ledRingPercentage.ledRingPercentage(12)

m.turnOn()
for i in range(0,100,6):
	l.showPercentage(i)
	time.sleep(0.25)
l.clear()
m.turnOff()
