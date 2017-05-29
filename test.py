import motor
import ledRingPercentage
import time

m = motor.motor(21)
l = ledRingPercentage.ledRingPercentage(12)

m.turnOn()
time.sleep(1)
m.turnOff()
time.sleep(1)
l.showPercentage(20)
time.sleep(1)
l.clear()
