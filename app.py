#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
import dht11
import ledRingPercentage as lrp
import motor
from psychrometricTable import getHR
from threading import Thread, Event
from time import sleep
import math

app = Flask(__name__)
app.config['SECRET KEY']='secret'
socketio = SocketIO(app)

m = motor.motor(13)
l = lrp.ledRingPercentage(18)
db = dht11.dht11(4)
wb = dht11.dht11(3)

thread = Thread()
thread_stop_event = Event()

class dhtUpdater(Thread):
	def __init__(self,db,lrp,wb):
		self.delay = 10
		self.db = db
		self.wb = wb
		self.lrp = lrp
		self.lrp.clear()
		super(dhtUpdater, self).__init__()
		
	def readAndUpdate(self):
		print 'reading dht'
		while not thread_stop_event.isSet():
			humdry, tempdry = self.db.readHumAndTemp()
			humwet, tempwet = self.wb.readHumAndTemp()
			humPMT = getHR(tempdry,tempwet)
			print 'humdry=',humdry,' tempdry=',tempdry
			print 'humwet=',humwet,' tempwet=',tempwet
			print 'humPMT=',humPMT
			if(humdry <= 100 and humwet <= 100):
				if(humdry < 60 and humPMT < 60 and abs(humdry-humPMT) < 5 or tempdry > 20):
					self.lrp.showPercentage(humdry);
					socketio.emit('update', {'humdry':humdry, 'tempdry':tempdry, 'humPMT':humPMT, 'motorStatus':1})
					m.turnOn()
					sleep(10)
					m.turnOff()
				self.lrp.showPercentage(humdry);
				socketio.emit('update', {'humdry':humdry, 'tempdry':tempdry, 'humPMT':humPMT, 'motorStatus':0})
			sleep(self.delay)
	
	def run(self):
		self.readAndUpdate()

@app.route("/")
def main():
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect')
def handle_dht11():
	global thread
	print 'Connected'
	if not thread.isAlive():
		print 'starting dht updater'
		thread = dhtUpdater(db=db, lrp=l, wb=wb)
		thread.start()

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received ' + str(json))
	
@socketio.on('toggleMotor')
def handle_my_custom_event(arg1):
	if (arg1 == 1):
		m.turnOn()
	elif(arg1 == 0):
		m.turnOff()
	

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8181, debug=True)
